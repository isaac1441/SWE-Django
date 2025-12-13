from django.conf import settings
from django.db import models
from django.db.models import Q

User = settings.AUTH_USER_MODEL

class DirectConversation(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dm_user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dm_user2")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user1", "user2"], name="unique_dm_pair"),
            models.CheckConstraint(check=~Q(user1=models.F("user2")), name="no_self_dm"),
        ]

    @staticmethod
    def canonical_pair(a, b):
        return (a, b) if a.id < b.id else (b, a)

    @classmethod
    def get_or_create_for_users(cls, a, b):
        u1, u2 = cls.canonical_pair(a, b)
        convo, _ = cls.objects.get_or_create(user1=u1, user2=u2)
        return convo

    def other_user(self, me):
        return self.user2 if me.id == self.user1_id else self.user1


class Message(models.Model):
    conversation = models.ForeignKey(
        DirectConversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
