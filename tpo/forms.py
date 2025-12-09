from django import forms
from student.models import Job
from .models import Announcement


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "company", "location", "description", "last_date"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "last_date": forms.DateInput(attrs={"type": "date"}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "message", "is_active"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4}),
        }