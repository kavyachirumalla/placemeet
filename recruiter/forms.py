# recruiter/forms.py
from django import forms
from django.utils import timezone

from student.models import StudentProfile
from .models import Interview


class StudentSearchForm(forms.Form):
    branch = forms.CharField(required=False)
    min_cgpa = forms.DecimalField(required=False, max_digits=4, decimal_places=2)
    skill = forms.CharField(required=False, help_text="Keyword in skills or resume")


class InterviewForm(forms.ModelForm):
    scheduled_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    class Meta:
        model = Interview
        fields = ["student", "job", "scheduled_at", "mode", "location", "note"]

    def clean_scheduled_at(self):
        dt = self.cleaned_data["scheduled_at"]
        if dt < timezone.now():
            raise forms.ValidationError("Schedule time must be in the future.")
        return dt