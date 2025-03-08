from django.db import models
from django.conf import settings
from django.utils import timezone

class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_messages')
    room_name = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"[{self.timestamp}] {self.user.username}: {self.content[:30]}"
