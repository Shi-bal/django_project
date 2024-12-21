import psycopg
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .utils import encrypt_message
from app2.models import Message




# Homepage view 
def homepage(request):
    return render(request, 'homepage.html')


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
            User.objects.create_user(username=username, email=email, password=password)
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


def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        message = request.POST.get('message')
        receiver_name = request.POST.get('receiver')  # Receiver name from form
        
        # Encrypt the message and the sender's username
        encrypted_message = encrypt_message(message)
        encrypted_sender_username = encrypt_message(request.user.username)

        # Save the message to the database
        Message.objects.create(
            plain_text=message,
            encrypted_text=encrypted_message,
            receiver=receiver_name,  # Save the receiver name as plain text
            sender=request.user,
        )
        
        return JsonResponse({"encrypted_message": encrypted_message})

    # Get all messages to display for the logged-in user
    messages = Message.objects.all()  # You can filter here if needed
    return render(request, 'dashboard.html', {'messages': messages})