from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Holiday model for local holiday management with yearly recurrence
class Holiday(models.Model):
    MONTH_CHOICES = [(i, f"{i:02d}") for i in range(1, 13)]
    DAY_CHOICES = [(i, f"{i:02d}") for i in range(1, 32)]
    
    # Keep original date field for backward compatibility (nullable)
    date = models.DateField(blank=True, null=True, help_text="Optional stored date (kept for backward compatibility)")

    month = models.IntegerField(choices=MONTH_CHOICES, help_text="Month (1-12)")
    day = models.IntegerField(choices=DAY_CHOICES, help_text="Day (1-31)")
    school_specific = models.BooleanField(default=False, help_text="Is this a school-declared date/event?")
    name = models.CharField(max_length=200, help_text="Holiday name (e.g., 'New Year's Day')")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['month', 'day']
        verbose_name_plural = 'Holidays'
        unique_together = ('month', 'day')  # Prevent duplicate holidays on same date

    def __str__(self):
        return f"{self.month:02d}-{self.day:02d} - {self.name}"
    
    def get_date_for_year(self, year):
        """Return the full date for this holiday in a given year"""
        from datetime import date
        try:
            return date(year, self.month, self.day)
        except ValueError:
            return None


class Schedule(models.Model):
    # Added department field and choices
    DEPARTMENT_CHOICES = [
        ('CCS', 'College of Computer Studies'),
        ('CMBA', 'College of Management, Business, and Accountancy'),
        ('CCJ', 'College of Criminal Justice'),
        ('CNAHS', 'College of Nursing and Allied Health Sciences'),
        ('CEA', 'College of Engineering and Architecture'),
        ('CASE', 'College of Arts, Sciences and Education'),
    ]

    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES,
        default='CCS'
    )

    professor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='schedules'
    )

    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    # UPDATED: canonical values you requested
    STATUS_CHOICES = [
        ('In Class', 'In Class'),
        ('Out of Work', 'Out of Work'),
        ('Available', 'Available'),
    ]

    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject_code = models.CharField(max_length=20)
    subject_name = models.CharField(max_length=100)
    section = models.CharField(max_length=50)
    room = models.CharField(max_length=50, blank=True, null=True)
    year_level = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.subject_code} - {self.subject_name} ({self.day})"

    def formatted_start_time(self):
        return self.start_time.strftime("%I:%M %p")

    def formatted_end_time(self):
        return self.end_time.strftime("%I:%M %p")


# Teacher profile model
class TeacherProfile(models.Model):
    DEPARTMENT_CHOICES = [
        ('BSIT_BSCS', 'BSIT / BSCS'),
        ('BS_Nursing', 'BS Nursing'),
        ('BS_CE', 'BS Civil Engineering'),
        ('BS_Arch', 'BS Architecture'),
        ('BS_Accountancy', 'BS Accountancy'),
        ('BS_Psychology', 'BS Psychology'),
        ('BS_Criminology', 'BS Criminology'),
        ('BS_Education', 'BS Education'),
        ('BS_Hospitality', 'BS Hospitality Management'),
        ('BS_Tourism', 'BS Tourism'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('absent', 'Absent'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    teacher_id = models.CharField(max_length=20, unique=True)
    contact_number = models.CharField(max_length=20)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.teacher_id})"


class StudentProfile(models.Model):
    COURSE_CHOICES = [
        ('BSIT', 'BSIT - Bachelor of Science in Information Technology'),
        ('BSCS', 'BSCS - Bachelor of Science in Computer Science'),
    ]

    YEAR_LEVEL_CHOICES = [
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    contact_number = models.CharField(max_length=20)
    course = models.CharField(max_length=10, choices=COURSE_CHOICES)
    year_level = models.CharField(max_length=10, choices=YEAR_LEVEL_CHOICES)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"
