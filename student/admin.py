from django.contrib import admin
from .models import (
    StudentProfile,
    Resume,
    Skill,
    Job,
    Application,
    Notification,
)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "branch", "cgpa", "graduation_year")
    search_fields = ("user__username", "full_name", "branch")
    list_filter = ("branch", "graduation_year")


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("student", "file", "uploaded_at")
    search_fields = ("student__user__username",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "student")
    search_fields = ("name", "student__user__username")


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "posted_at")
    search_fields = ("title", "company", "location")
    list_filter = ("company", "location")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("student", "job", "status", "applied_at")
    search_fields = ("student__user__username", "job__title", "job__company")
    list_filter = ("status",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "is_read", "created_at")
    search_fields = ("user__username", "message")
    list_filter = ("is_read", "created_at")