from django.db import models

# Create your models here.
# tpo/models.py
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Announcement(models.Model):
    tpo = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="announcements",
    )
    title = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.tpo})"