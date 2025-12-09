from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import StudentProfile, Job, Application, Notification, Skill
from .forms import StudentProfileForm, SkillForm


@login_required
def student_dashboard(request):
    user = request.user

    # safety: only students should be here
    if getattr(user, "role", None) != "student":
        return redirect('users:index')

    profile, _ = StudentProfile.objects.get_or_create(
        user=user,
        defaults={"full_name": user.get_full_name() or user.username}
    )

    profile_form = StudentProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=profile
    )

    skill_form = SkillForm(request.POST or None)

    if request.method == "POST":
        if "save_profile" in request.POST and profile_form.is_valid():
            profile_form.save()
            return redirect('student:student_dashboard')

        if "add_skill" in request.POST and skill_form.is_valid():
            skill = skill_form.save(commit=False)
            skill.student = profile
            skill.save()
            return redirect('student:student_dashboard')

    skills = profile.skills.all()
    jobs = Job.objects.all().order_by("-posted_at")[:5]
    applications = Application.objects.filter(student=profile).select_related("job")
    notifications = Notification.objects.filter(user=user).order_by("-created_at")[:5]

    # profile completion % (name, phone, branch, resume, cgpa, graduation_year)
    fields = [
        bool(profile.full_name),
        bool(profile.phone),
        bool(profile.branch),
        bool(profile.cgpa),
        bool(profile.graduation_year),
    ]
    filled = sum(1 for f in fields if f)
    total = len(fields)
    profile_completion = int((filled / total) * 100) if total else 0

    context = {
        "profile": profile,
        "profile_form": profile_form,
        "skill_form": skill_form,
        "skills": skills,
        "jobs": jobs,
        "applications": applications,
        "notifications": notifications,
        "profile_completion": profile_completion,
        "applied_count": applications.count(),
        "notify_count": notifications.count(),
    }
    return render(request, 'student-dashboard.html', context)