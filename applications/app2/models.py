from django.db import models

class Message(models.Model):
    plain_text = models.TextField()
    encrypted_text = models.TextField()
    receiver = models.CharField(max_length=255)  # As receiver doesn't need to be registered user
    sender = models.CharField(max_length=255)  # To store the encrypted sender username
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # Field to mark if the message is approved

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} - Approved: {self.is_approved}"
