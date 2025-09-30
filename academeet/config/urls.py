from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import RedirectView
from ui import views as ui_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='role_selection', permanent=False)),
    path('role-selection/', ui_views.role_selection, name='role_selection'),
    path('student-login/', ui_views.student_login, name='student_login'),
    path('teacher-login/', ui_views.teacher_login, name='teacher_login'),
    path('signup/student/', ui_views.student_signup, name='student_signup'),
    path('signup/teacher/', ui_views.teacher_signup, name='teacher_signup'),
    path('forgotpassword/', ui_views.forgot_password, name='forgot_password'),
    path('forgot-password/', ui_views.forgot_password),
    path('reset/', ui_views.reset_password, name='reset_password'),
    path('reset-success/', ui_views.reset_password_success, name='reset_password_success'),
]
