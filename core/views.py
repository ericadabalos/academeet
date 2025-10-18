from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import get_messages

#NEW SCHEDULE
#from datetime import datetime, timedelta


User = get_user_model()


def home(request):
    # role selection page
    return render(request, 'role_selection.html')


def student_signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not email or not password1 or password1 != password2:
            return render(request, 'student_signup.html', {'error': 'Please provide matching passwords and an email.'})

        if User.objects.filter(username=email).exists():
            messages.warning(request, 'An account with that email already exists. Please login.')
            return redirect('student_login')

        user = User.objects.create_user(username=email, email=email, password=password1, first_name=full_name or '')
        messages.success(request, 'Student account created. Please log in.')
        return redirect('student_login')

    return render(request, 'student_signup.html')


def teacher_signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not email or not password1 or password1 != password2:
            return render(request, 'teacher_signup.html', {'error': 'Please provide matching passwords and an email.'})

        if User.objects.filter(username=email).exists():
            messages.warning(request, 'An account with that email already exists. Please login.')
            return redirect('teacher_login')

        user = User.objects.create_user(username=email, email=email, password=password1, first_name=full_name or '')
        messages.success(request, 'Teacher account created. Please log in.')
        return redirect('teacher_login')

    return render(request, 'teacher_signup.html')


def student_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        # Distinguish between "not registered" and "wrong password"
        if not User.objects.filter(username=email).exists():
            return render(request, 'student_login.html', {'error': 'Email not registered. Please sign up.'})
        else:
            return render(request, 'student_login.html', {'error': 'Incorrect password. Please try again.'})

    return render(request, 'student_login.html')


def teacher_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Welcome back! Redirecting to professor dashboard.')
            return redirect('professor_dashboard')
        # Distinguish between "not registered" and "wrong password"
        if not User.objects.filter(username=email).exists():
            return render(request, 'teacher_login.html', {'error': 'Email not registered. Please sign up.'})
        else:
            return render(request, 'teacher_login.html', {'error': 'Incorrect password. Please try again.'})

    return render(request, 'teacher_login.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # In this simplified flow we won't send real emails. Store the email in session
        request.session['pw_reset_email'] = email
        # Could set a cooldown timestamp here
        return redirect('forgot_password_sent')
    return render(request, 'forgot_password_page.html')


def forgot_password_sent(request):
    email = request.session.get('pw_reset_email')
    cooldown_remaining = 0
    if request.method == 'POST':
        # Simulate resend: keep the same email in session
        request.session['pw_reset_email'] = request.POST.get('email', email)
        # In a real app you'd re-send an email and set a cooldown
        cooldown_remaining = 90

    return render(request, 'forgot_password_sent.html', {'email': email, 'cooldown_remaining': cooldown_remaining})


def reset_password(request):
    # For simplicity this view accepts an ?email=... GET param to identify the user.
    email = request.GET.get('email') or request.session.get('pw_reset_email')
    if request.method == 'POST':
        new = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')
        if not new or new != confirm:
            return render(request, 'reset_password.html', {'error': 'Passwords do not match.'})
        if not email:
            return render(request, 'reset_password.html', {'error': 'No email specified.'})
        try:
            user = User.objects.get(username=email)
            user.set_password(new)
            user.save()
            return redirect('reset_password_success')
        except User.DoesNotExist:
            return render(request, 'reset_password.html', {'error': 'User not found.'})

    return render(request, 'reset_password.html')


def reset_password_success(request):
    return render(request, 'reset_password_success.html')


@login_required
#def dashboard(request):
 #   return render(request, 'dashboard.html')

#NEW STUDENT DASHBOARD
def dashboard(request):
    start_hour = 7
    end_hour = 21.5  # 9:30 PM
    hours = []
    time = start_hour
    while time <= end_hour:
        hour = int(time)
        minute = int((time - hour) * 60)
        suffix = "AM" if hour < 12 else "PM"
        display_hour = hour if hour <= 12 else hour - 12
        time_str = f"{display_hour}:{minute:02d} {suffix}"
        hours.append(time_str)
        time += 0.5

    # add user_name to the template context as you requested
    user_name = (request.user.get_full_name() or request.user.username) if request.user.is_authenticated else ""
    return render(request, "dashboard.html", {"hours": hours, "user_name": user_name})


def logout_view(request):
    logout(request)
    return render(request, "redirectingafterlogout_page.html")



@login_required
def professor_dashboard(request):
    # Show the professor dashboard template; use user's name if available
    return render(request, 'professor_dashboard.html', {
        'user_name': request.user.get_full_name() or request.user.username
    })


def logout_view(request):
    """Log out the current user and redirect to role selection."""
    auth_logout(request)
    # Clear any pending messages so they don't appear on the role selection page
    # after the automatic redirect chain (logout -> notice -> protected dashboard -> login redirect).
    storage = get_messages(request)
    # iterating consumes the messages
    for _ in storage:
        pass

    # Render a short notice page that then redirects to the professor dashboard
    return render(request, 'redirectingafterlogout_page.html')

from django.shortcuts import render
from django.contrib.auth import logout



