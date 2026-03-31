# billing/models.py

from django.db import models
from django.contrib.auth.models import User

class MessMenu(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    day = models.CharField(max_length=10, choices=DAY_CHOICES, unique=True)
    breakfast = models.CharField(max_length=200)
    lunch = models.CharField(max_length=200)
    dinner = models.CharField(max_length=200)

    def __str__(self):
        return self.day

class AttendanceSummary(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_summaries')
    month = models.IntegerField() # 1-12
    year = models.IntegerField()
    total_present_days = models.IntegerField(default=0)
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('student', 'month', 'year')

    def save(self, *args, **kwargs):
        # Calculation: 100 per present day
        self.bill_amount = self.total_present_days * 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.username} - {self.month}/{self.year}: {self.total_present_days} days"

class PaymentRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('REJECTED', 'Rejected'),
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    summary = models.ForeignKey(AttendanceSummary, on_delete=models.SET_NULL, null=True, blank=True)
    screenshot = models.ImageField(upload_to='payment_screenshots/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.username} - {self.status}"

class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    is_present = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.username} - {self.date}"
