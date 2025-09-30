from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# import your model + form
from .models import Schedule
from .forms import ScheduleForm


# ---------------- AUTH VIEWS ---------------- #

def login_view(request):
    # Step 1: Determine the role (priority: POST > GET > session)
    role = request.POST.get("role") or request.GET.get("role") or request.session.get("role")

    # Step 2: Save role in session if provided
    if role:
        request.session["role"] = role

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Step 3: Redirect based on role
            if role == "student":
                return redirect("student_dashboard")
            elif role == "professor":
                return redirect("professor_dashboard")
            else:
                return redirect("dashboard")  # fallback if no role
        else:
            messages.error(request, "Invalid username or password")

    # Step 4: If no role at all, force them to role selection
    if not role:
        return redirect("role_selection")

    return render(request, "core/login.html", {"role": role})


def register_view(request):
    """Handles user registration"""
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

    return render(request, "core/register.html")


@login_required
def dashboard_view(request):
    """Generic dashboard (for now)"""
    return render(request, "core/dashboard.html")


def logout_view(request):
    """Logs out the current user"""
    logout(request)
    return redirect('login')


def role_selection(request):
    """Landing page for role selection"""
    return render(request, 'core/role_selection.html')


def student_dashboard(request):
    """Student dashboard view"""
    return render(request, "core/student_dashboard.html")


def professor_dashboard(request):
    """Professor dashboard view"""
    return render(request, "core/professor_dashboard.html")


# ---------------- SCHEDULE VIEWS ---------------- #

@login_required
def schedule_list(request):
    schedules = Schedule.objects.all().order_by("day", "start_time")
    return render(request, "core/schedule_list.html", {"schedules": schedules})


@login_required
def add_schedule(request):
    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Schedule added successfully!")
            return redirect("schedule_list")
    else:
        form = ScheduleForm()
    return render(request, "core/schedule_form.html", {"form": form})


@login_required
def edit_schedule(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.method == "POST":
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, "Schedule updated successfully!")
            return redirect("schedule_list")
    else:
        form = ScheduleForm(instance=schedule)
    return render(request, "core/schedule_form.html", {"form": form})
