from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import time
import hashlib
import secrets


def role_selection(request: HttpRequest) -> HttpResponse:
    return render(request, 'role_selection.html')


def student_login(request: HttpRequest) -> HttpResponse:
    return render(request, 'student_login.html')


def teacher_login(request: HttpRequest) -> HttpResponse:
    return render(request, 'teacher_login.html')


def student_signup(request: HttpRequest) -> HttpResponse:
    return render(request, 'student_signup.html')

def teacher_signup(request: HttpRequest) -> HttpResponse:
    return render(request, 'teacher_signup.html')

def forgot_password(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        # If an email is provided, send a reset email and remember it for possible resend
        email = request.POST.get('email')
        COOLDOWN_SECONDS = 90
        now_epoch = int(time.time())
        last_sent_epoch = request.session.get('last_reset_sent_at')
        cooldown_remaining = 0

        if email:
            subject = 'Your password reset link'
            message = (
                'We received a request to reset your password.\n\n'
                'Use this link to proceed: http://localhost:8000/reset/?email=' + email + '\n\n'
                'If you did not request a password reset, you can ignore this message.'
            )
            # Always send email and reset cooldown for new requests
            send_mail(subject, message, getattr(settings, 'DEFAULT_FROM_EMAIL', None), [email], fail_silently=True)
            request.session['last_reset_sent_at'] = now_epoch
            cooldown_remaining = COOLDOWN_SECONDS
            request.session['reset_email'] = email
            return render(request, 'forgot_password_sent.html', { 'email': email, 'cooldown_remaining': cooldown_remaining })
        else:
            # Resend if we have a stored email in the session
            session_email = request.session.get('reset_email')
            if session_email:
                subject = 'Your password reset link (resend)'
                message = (
                    'Here is your password reset link again.\n\n'
                    'Link: http://localhost:8000/reset/?email=' + session_email
                )
                # Always reset the timer when requesting a new link
                send_mail(subject, message, getattr(settings, 'DEFAULT_FROM_EMAIL', None), [session_email], fail_silently=True)
                request.session['last_reset_sent_at'] = now_epoch
                cooldown_remaining = COOLDOWN_SECONDS
            return render(request, 'forgot_password_sent.html', { 'email': session_email, 'cooldown_remaining': cooldown_remaining })
    return render(request, 'forgot_password_page.html')


def reset_password(request: HttpRequest) -> HttpResponse:
    """Handle password reset form and processing"""
    if request.method == 'POST':
        email = request.GET.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not email:
            return render(request, 'reset_password.html', {'error': 'Invalid reset link'})
        
        if new_password != confirm_password:
            return render(request, 'reset_password.html', {'error': 'Passwords do not match'})
        
        if len(new_password) < 8:
            return render(request, 'reset_password.html', {'error': 'Password must be at least 8 characters long'})
        
        # In a real application, you would verify the reset token here
        # For now, we'll just update the password if the user exists
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return redirect('reset_password_success')
        except User.DoesNotExist:
            return render(request, 'reset_password.html', {'error': 'User not found'})
    
    # GET request - show the reset form
    email = request.GET.get('email')
    if not email:
        return render(request, 'reset_password.html', {'error': 'Invalid reset link'})
    
    return render(request, 'reset_password.html', {'email': email})


def reset_password_success(request: HttpRequest) -> HttpResponse:
    """Show password reset success page"""
    return render(request, 'reset_password_success.html')
