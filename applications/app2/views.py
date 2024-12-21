from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import CustomUserCreationForm
from .utils import decrypt_message




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
    # Fetch messages for the logged-in user
    messages = Message.objects.filter(is_approved=False)

    decrypted_messages = []
    for message in messages:
        try:
            decrypted_content = decrypt_message(message.encrypted_text)
            decrypted_messages.append({
            "id": message.id,
            "content": decrypted_content,
            "sender": message.sender,
        })
        except Exception as e:
            print(f"Error decrypting message ID {message.id}: {e}")


    # Handle POST request to approve messages
    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        if message_id:
            try:
                message = Message.objects.get(id=message_id)
                message.is_approved = True
                message.save()
            except Message.DoesNotExist:
                return render(request, 'app2/error.html', {"error": "Message not found."})

        # Redirect to avoid re-submission of the form
        return redirect('message_list')

    # Render the template for GET requests
    return render(request, 'app2/message_list.html', {'messages': decrypted_messages})

