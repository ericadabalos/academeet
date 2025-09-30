from django.urls import path
from . import views

urlpatterns = [
    # Role selection as landing page
    path('', views.role_selection, name='role_selection'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboards by role
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('professor/dashboard/', views.professor_dashboard, name='professor_dashboard'),

    # Schedule management (professor only)
    path('schedules/add/', views.add_schedule, name='add_schedule'),
    path('schedules/<int:pk>/edit/', views.edit_schedule, name='edit_schedule'),
]
