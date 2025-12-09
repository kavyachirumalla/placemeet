# Create your models here.
# recruiter/models.py
from django.conf import settings
from django.db import models
from django.utils import timezone

from student.models import StudentProfile, Application
from student.models import Job   

class RecruiterProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recruiter_profile",
    )
    company_name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150, blank=True)
    contact_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.company_name} ({self.user.username})"


class Interview(models.Model):
    recruiter = models.ForeignKey(
        RecruiterProfile, on_delete=models.CASCADE, related_name="interviews"
    )
    student = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE, related_name="interviews"
    )
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="interviews"
    )
    scheduled_at = models.DateTimeField()
    mode = models.CharField(
        max_length=50,
        choices=(
            ("online", "Online"),
            ("offline", "Offline"),
        ),
        default="online",
    )
    location = models.CharField(max_length=200, blank=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student.user.username} - {self.job.title} @ {self.scheduled_at}"