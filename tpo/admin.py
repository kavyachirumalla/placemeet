from django.contrib import admin
from .models import Announcement

# Register your models here.



@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "tpo", "created_at", "is_active")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "message", "tpo__username")