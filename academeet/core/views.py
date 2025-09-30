from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import secrets
import string

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')   # redirect to dashboard
        messages.error(request, "Invalid username or password")
    return render(request, "login.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("register")
        User.objects.create_user(username=username, password=password)
        messages.success(request, "Registration successful! Please login.")
        return redirect("login")
    return render(request, "register.html")

@login_required
def dashboard_view(request):
    return render(request, "dashboard.html")

def logout_view(request):
    logout(request)
    return redirect('login')

def forgot_password_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        try:
            user = User.objects.get(username=username)
            # Generate a temporary password
            temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
            user.set_password(temp_password)
            user.save()
            
            # In a real application, you would send this via email
            # For now, we'll just show it in a message
            messages.success(request, f"Temporary password for {username}: {temp_password}")
            messages.info(request, "Please login with this temporary password and change it immediately.")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "Username not found")
    
    return render(request, "forgot_password.html")
