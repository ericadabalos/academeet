from django.db import models
from django.utils import timezone

class Schedule(models.Model):
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    YEAR_LEVEL_CHOICES = [
        (1, '1st Year'),
        (2, '2nd Year'),
        (3, '3rd Year'),
        (4, '4th Year'),
    ]

    STATUS_CHOICES = [
        ('in_class', 'In Class'),
        ('busy', 'Busy'),
        ('absent', 'Absent'),
        ('available', 'Available'),
    ]

    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK, default='monday')
    start_time = models.TimeField(default="07:00:00")
    end_time = models.TimeField(default="08:00:00")
    subject = models.CharField(max_length=100, default="TBA")
    room = models.CharField(max_length=50, default="TBA")  # ✅ Default so no migration error
    year_level = models.IntegerField(choices=YEAR_LEVEL_CHOICES, default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_day_display()} {self.start_time}-{self.end_time} | {self.subject}"
