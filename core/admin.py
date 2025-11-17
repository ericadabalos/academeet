from django.contrib import admin
from .models import Schedule, Holiday, TeacherProfile, StudentProfile


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('month', 'day', 'name', 'description', 'school_specific', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('month', 'school_specific', 'created_at')
    ordering = ('month', 'day')

    fieldsets = (
        ('Holiday Information', {
            'fields': ('month', 'day', 'name', 'description', 'school_specific')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('subject_code', 'professor', 'day', 'start_time', 'end_time', 'status')
    search_fields = ('subject_code', 'subject_name', 'professor__username')
    list_filter = ('day', 'status', 'department')
    ordering = ('day', 'start_time')


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'teacher_id', 'department', 'status')
    search_fields = ('user__username', 'teacher_id')
    list_filter = ('department', 'status')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'course', 'year_level')
    search_fields = ('user__username', 'student_id')
    list_filter = ('course', 'year_level')
