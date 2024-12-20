from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import CustomUserCreationForm


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'app2/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('message_list')
    else:
        form = AuthenticationForm()
    return render(request, 'app2/login.html', {'form': form})

@login_required
def message_list(request):
    # Fetch all unapproved messages
    messages = Message.objects.filter(is_approved=False)

    if request.method == 'POST':
        # Get the message ID from the form and update its status to approved
        message_id = request.POST.get('message_id')
        message = Message.objects.get(id=message_id)
        message.is_approved = True
        message.save()

    return render(request, 'app2/message_list.html', {'messages': messages})
