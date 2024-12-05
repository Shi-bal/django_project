from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .utils import encrypt_message
from .models import Message  # Import the Message model





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


# app1/views.py
def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        message = request.POST.get('message')
        
        # Encrypt the message
        encrypted_message = encrypt_message(message)
        
        # Save the message to the database
        Message.objects.create(
            plain_text=message,
            encrypted_text=encrypted_message
        )
        
        return JsonResponse({"encrypted_message": encrypted_message})

    # Get all messages to display
    messages = Message.objects.all()
    return render(request, 'dashboard.html', {'messages': messages})
