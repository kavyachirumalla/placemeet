from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User


def index(request):
    return render(request, 'index.html')


def login_page(request):
    # separate view just to render template (GET)
    return render(request, 'login.html')


def login_view(request):
    if request.method != 'POST':
        return redirect('users:login')

    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)

    if user is None:
        messages.error(request, "Invalid username or password.")
        return render(request, 'login.html')

    login(request, user)

    # Role-based redirect
    if user.role == 'student':
        return redirect('student:student_dashboard')
    elif user.role == 'tpo':
        # you’ll create tpo dashboard later
        return redirect('tpo:tpo_dashboard')
    elif user.role == 'recruiter':
        # recruiter dashboard later
        return redirect('recruiter:recruiter_dashboard')

    # fallback
    return redirect('index')


@login_required
def logout_view(request):
    logout(request)
    return redirect('users:login')