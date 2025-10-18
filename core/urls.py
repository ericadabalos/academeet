from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='role_selection'),
    path('student/signup/', views.student_signup, name='student_signup'),
    path('teacher/signup/', views.teacher_signup, name='teacher_signup'),
    path('student/login/', views.student_login, name='student_login'),
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('forgot-password/sent/', views.forgot_password_sent, name='forgot_password_sent'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('reset-password/success/', views.reset_password_success, name='reset_password_success'),
    
    #path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('professor/dashboard/', views.professor_dashboard, name='professor_dashboard'),
    path('logout/', views.logout_view, name='logout'),
]
