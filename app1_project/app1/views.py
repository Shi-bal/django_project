from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .utils import encrypt_message




# Homepage view 
def homepage(request):
    return render(request, 'homepage.html')


# Registration View
def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)
            return redirect('login')
        else:
            return render(request, 'register.html', {"error": "Username already exists!"})
    return render(request, 'register.html')

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {"error": "Invalid credentials!"})
    return render(request, 'login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard View (Page after Login)
def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        message = request.POST.get('message')
        encrypted_message = encrypt_message(message)
        # Simulate sending the message (you can add logic to send it to another app)
        return JsonResponse({"encrypted_message": encrypted_message})
    return render(request, 'dashboard.html')
