from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

User = get_user_model()

@login_required(login_url='admin_login')
def admin_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('/')

    # Filtering
    role = request.GET.get('role')
    status = request.GET.get('status')

    users = User.objects.all()

    if role and role.lower() in ["student", "professor"]:
        users = users.filter(role__iexact=role)
    if status == "active":
        users = users.filter(is_active=True)
    elif status == "deactivated":
        users = users.filter(is_active=False)

    context = {
        'users': users,
        'user_name': request.user.get_full_name() or request.user.username,
    }
    return render(request, 'admin_dashboard.html', context)


@login_required(login_url='admin_login')
def toggle_user_status(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized action.")
        return redirect('admin_dashboard')

    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()

    if user.is_active:
        messages.success(request, f"{user.email} has been activated.")
    else:
        messages.warning(request, f"{user.email} has been deactivated.")

    return redirect('admin_dashboard')

from django.contrib.auth import authenticate, login

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials or not an admin.")
            return redirect('admin_login')

    return render(request, 'admin_dashboard.html')
