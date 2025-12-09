from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings

User = get_user_model()  # this is your custom users.User


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    full_name = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    graduation_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.full_name or self.user.username


class Resume(models.Model):
    student = models.OneToOneField(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="resume",
    )
    file = models.FileField(upload_to="resumes/", blank=True, null=True)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Resume of {self.student.user.username}"


class Skill(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="skills",
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.student.user.username})"


class Job(models.Model):
    title = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="posted_jobs",
    )
    last_date=models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.company}"


class Application(models.Model):
    STATUS_CHOICES = (
        ("applied", "Applied"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
        ("selected", "Selected"),
    )

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="applied",
    )

    def __str__(self):
        return f"{self.student.user.username} → {self.job.title} ({self.status})"


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="student_notifications",
    )
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}: {self.message[:30]}"