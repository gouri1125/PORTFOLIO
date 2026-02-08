from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from .models import Skill, Project, ContactMessage

User = get_user_model()

# ==========================
# SUPERUSER DECORATOR
# ==========================

def superuser_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_superuser,
        login_url='portfolio_app:login'
    )(view_func)

# ==========================
# AUTHENTICATION VIEWS
# ==========================

def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                f"Welcome, {user.username}! Your account has been created."
            )

            # 🔐 Superuser → dashboard, normal user → home
            if user.is_superuser:
                return redirect('portfolio_app:dashboard')
            return redirect('portfolio_app:home')

        messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'portfolio_app/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('portfolio_app:dashboard')
        return redirect('portfolio_app:home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")

            if user.is_superuser:
                return redirect('portfolio_app:dashboard')
            else:
                return redirect('portfolio_app:home')
            
        messages.error(request, "Invalid username or password.")

    return render(request, 'portfolio_app/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('portfolio_app:home')

# ==========================
# PUBLIC PAGES
# ==========================

def home(request):
    return render(request, 'portfolio_app/home.html')


def about(request):
    return render(request, 'portfolio_app/about.html')


def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            message=request.POST.get('message')
        )
        messages.success(request, 'Message sent successfully!')
        return redirect('portfolio_app:contact')

    return render(request, 'portfolio_app/contact.html')

# ==========================
# SUPERUSER DASHBOARD
# ==========================

@superuser_required
def dashboard(request):
    context = {
        'projects_count': Project.objects.count(),
        'skills_count': Skill.objects.count(),
        'messages_count': ContactMessage.objects.filter(is_read=False).count(),
        'user_count': User.objects.count(),
        'projects': Project.objects.all(),
        'skills': Skill.objects.all(),
    }
    return render(request, 'portfolio_app/dashboard.html', context)

# ==========================
# LOGGED-IN USERS (VIEW ONLY)
# ==========================

@login_required
def skills_view(request):
    skills = Skill.objects.all()
    return render(request, 'portfolio_app/skills.html', {'skills': skills})


@login_required
def projects_view(request):
    projects = Project.objects.all()
    return render(request, 'portfolio_app/projects.html', {'projects': projects})
