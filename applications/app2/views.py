from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import CustomUserCreationForm
from .utils import decrypt_message
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages as django_messages  # Renamed import
from django.core.mail import mail_managers, mail_admins
from .decorators import app2_login_required
from datetime import datetime


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app2:login')  # Redirect to login after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'app2/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            request.session['app2_user'] = user.username
            request.session['app2_login_time'] = str(datetime.now())
            return redirect('app2:message_list')
    else:
        form = AuthenticationForm()
    return render(request, 'app2/login.html', {'form': form})

@app2_login_required
def message_list(request):
    message_queryset = Message.objects.filter(is_approved=False)
    
    decrypted_messages = []
    for message in message_queryset:
        try:
            decrypted_content = decrypt_message(message.encrypted_text)
            decrypted_messages.append({
                "id": message.id,
                "content": decrypted_content,
                "sender": message.sender,
            })
        except Exception as e:
            print(f"Error decrypting message ID {message.id}: {e}")

    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        if message_id:
            try:
                message = Message.objects.get(id=message_id)
                message.is_approved = True
                message.save()
                
                # Using the renamed import
                django_messages.success(request, f'Message {message_id} has been approved successfully.')

            except Message.DoesNotExist:
                return render(request, 'app2/error.html', {"error": "Message not found."})

        return redirect('app2:message_list')

    # Render the template for GET requests
    return render(request, 'app2/message_list.html', {'messages': decrypted_messages})

def logout_user(request):
    if 'app2_user' in request.session:
        del request.session['app2_user']
        del request.session['app2_login_time']
    logout(request)
    return redirect('app2:login')


