# Register your models here.
from django.contrib import admin
from .models import RecruiterProfile, Interview


@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "company_name", "designation", "contact_email", "phone")
    search_fields = ("user__username", "company_name")


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ("student", "job", "recruiter", "scheduled_at", "mode")
    list_filter = ("mode", "scheduled_at")
    search_fields = ("student__user__username", "job__title", "recruiter__company_name")