from django import forms
from .models import StudentProfile, Skill


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['full_name', 'phone', 'branch', 'cgpa', 'graduation_year', ]


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter skill'})
        }