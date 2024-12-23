import psycopg
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .utils import encrypt_message
from app2.models import Message
from .decorators import app1_login_required
from datetime import datetime
from django.utils import timezone
from django.conf import settings




# Homepage view 
def homepage(request):
    messages = Message.objects.filter(is_approved=True)
    return render(request, 'homepage.html', {'messages': messages})



# Registration View
def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            return render(request, 'register.html', {"error": "Passwords do not match!"})

        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {"error": "Email is already registered!"})

        # Check if username already exists
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, email=email, password=password)
            request.session['user_id'] = user.id
            request.session['username'] = username
            return redirect('app1:login')
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
            request.session['app1_user'] = username
            request.session['app1_last_login'] = str(datetime.now())
            return redirect('app1:dashboard')
        else:
            return render(request, 'login.html', {"error": "Invalid credentials!"})
    return render(request, 'login.html')

# Logout View
def logout_view(request):
    if 'app1_user' in request.session:
        del request.session['app1_user']
        del request.session['app1_last_login']
    logout(request)
    return redirect('app1:login')


@app1_login_required
def dashboard_view(request):
    if not request.user.is_authenticated or 'app1_user' not in request.session:
        return redirect('app1:login')

    if request.method == "POST":
        message = request.POST.get('message')
        receiver_name = request.POST.get('receiver')  # Receiver name from form
        
        # Encrypt the message and the sender's username
        encrypted_message = encrypt_message(message)
        encrypted_sender_username = encrypt_message(request.session['app1_user'])

        # Save the message to the database
        Message.objects.create(
            plain_text=message,
            encrypted_text=encrypted_message,
            receiver=receiver_name,  # Save the receiver name as plain text
            sender=request.user,
        )

    # Get all messages to display for the logged-in user
    messages = Message.objects.all()  # You can filter here if needed
    return render(request, 'dashboard.html', {'messages': messages})