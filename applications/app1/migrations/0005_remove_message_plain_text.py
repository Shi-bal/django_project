# Generated by Django 5.1.4 on 2024-12-20 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_remove_message_sender_username_encrypted_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='plain_text',
        ),
    ]