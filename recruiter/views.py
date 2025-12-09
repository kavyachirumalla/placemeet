# Create your views here.
# recruiter/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

from student.models import StudentProfile, Application, Skill
from student.models import Job
from .models import RecruiterProfile
from .forms import StudentSearchForm, InterviewForm


@login_required
def recruiter_dashboard(request):
    # Only recruiters allowed here
    if getattr(request.user, "role", None) != "recruiter":
        return HttpResponseForbidden("Not allowed")

    # Ensure recruiter profile exists
    recruiter_profile, _ = RecruiterProfile.objects.get_or_create(
        user=request.user,
        defaults={"company_name": request.user.username},
    )

    # Jobs posted for this recruiter (assuming Job has posted_by FK)
    jobs_qs = Job.objects.filter(posted_by=request.user)

    # Applications for those jobs
    applications_qs = Application.objects.filter(job__in=jobs_qs)

    # Card counts
    eligible_candidates = StudentProfile.objects.count()  # simple version
    shortlisted_count = applications_qs.filter(status="shortlisted").count()
    total_applications = applications_qs.count()

    # ---- Student search ----
    search_form = StudentSearchForm(request.GET or None)
    search_results = StudentProfile.objects.none()

    if search_form.is_valid():
        qs = StudentProfile.objects.all()
        branch = search_form.cleaned_data.get("branch")
        min_cgpa = search_form.cleaned_data.get("min_cgpa")
        skill = search_form.cleaned_data.get("skill")

        if branch:
            qs = qs.filter(branch__icontains=branch)
        if min_cgpa is not None:
            qs = qs.filter(cgpa__gte=min_cgpa)
        if skill:
            qs = qs.filter(
                skills__name__icontains=skill
            ).distinct()  # Skill model linked with related_name="skills"

        search_results = qs

    # ---- Schedule interview ----
    interview_form = InterviewForm(request.POST or None)
    if request.method == "POST" and "schedule_interview" in request.POST:
        if interview_form.is_valid():
            interview = interview_form.save(commit=False)
            interview.recruiter = recruiter_profile
            interview.save()
            # later you can create Notification for student here
            return redirect("recruiter:recruiter_dashboard")

    context = {
        "recruiter_profile": recruiter_profile,
        "eligible_candidates": eligible_candidates,
        "shortlisted_count": shortlisted_count,
        "total_applications": total_applications,
        "jobs": jobs_qs,
        "applications": applications_qs.select_related("student", "job"),
        "search_form": search_form,
        "search_results": search_results,
        "interview_form": interview_form,
    }
    return render(request, "recruiter_dashboard.html", context)