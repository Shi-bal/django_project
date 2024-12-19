from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    plain_text = models.TextField()
    encrypted_text = models.TextField()
    receiver = models.CharField(max_length=255)  # Receiver name as plain text
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    created_at = models.DateTimeField(auto_now_add=True)
