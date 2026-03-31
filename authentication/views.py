from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/')
        elif request.user.is_staff:
            return redirect('billing:staff_dashboard')
        else:
            return redirect('billing:student_dashboard')
    return render(request, 'authentication/index.html')

def user_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/')
        elif request.user.is_staff:
            return redirect('billing:staff_dashboard')
        else:
            return redirect('billing:student_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')
            elif user.is_staff:
                return redirect('billing:staff_dashboard')
            else:
                return redirect('billing:student_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'authentication/login.html')

def user_registration(request):
    # Registration is disabled as per user request (no option for register only login)
    messages.warning(request, 'Registration is currently disabled.')
    return redirect('authentication:login')

def user_logout(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('authentication:login')