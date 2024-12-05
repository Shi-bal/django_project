# app1/models.py
from django.db import models

class Message(models.Model):
    plain_text = models.TextField()  # To store the plain message
    encrypted_text = models.TextField()  # To store the encrypted message
    created_at = models.DateTimeField(auto_now_add=True)  # To store the timestamp

    def __str__(self):
        return self.plain_text[:50]  # Display the first 50 characters of the plain text
