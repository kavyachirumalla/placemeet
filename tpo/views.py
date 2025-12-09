

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

from student.models import StudentProfile, Job, Application
from .models import Announcement
from .forms import JobForm, AnnouncementForm


@login_required
def tpo_dashboard(request):
    # allow only TPO users
    if getattr(request.user, "role", None) != "tpo":
        return HttpResponseForbidden("Not allowed")

    # --- counts for cards ---
    total_students = StudentProfile.objects.count()
    jobs_posted = Job.objects.filter(posted_by=request.user).count()
    pending_apps = Application.objects.filter(status="pending").count()
    shortlisted = Application.objects.filter(status="shortlisted").count()
    companies_visited = Job.objects.filter(posted_by=request.user).values("company").distinct().count()
    placed_students = (
        Application.objects.filter(status="selected")
        .values("student")
        .distinct()
        .count()
    )

    # --- forms / actions ---
    job_form = JobForm(request.POST or None)
    ann_form = AnnouncementForm(request.POST or None)

    if request.method == "POST":
        if "post_job" in request.POST and job_form.is_valid():
            job = job_form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect("tpo:tpo_dashboard")

        if "post_announcement" in request.POST and ann_form.is_valid():
            ann = ann_form.save(commit=False)
            ann.tpo = request.user
            ann.save()
            return redirect("tpo:tpo_dashboard")

    # list data
    students = StudentProfile.objects.select_related("user").order_by("full_name")
    announcements = Announcement.objects.filter(is_active=True)[:10]

    context = {
        "total_students": total_students,
        "jobs_posted": jobs_posted,
        "pending_apps": pending_apps,
        "shortlisted": shortlisted,
        "companies_visited": companies_visited,
        "placed_students": placed_students,
        "job_form": job_form,
        "ann_form": ann_form,
        "students": students,
        "announcements": announcements,
    }
    return render(request, "tpo-dashboard.html", context)