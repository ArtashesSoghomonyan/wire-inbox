import uuid

from django.db import models
from users.models import User


class DirectConversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant_1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="direct_conversations_as_participant_1",
    )
    participant_2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="direct_conversations_as_participant_2",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.participant_1.username} - {self.participant_2.username}"

    def save(self, *args, **kwargs):
        participant_1_id = getattr(self, "participant_1_id", None)
        participant_2_id = getattr(self, "participant_2_id", None)

        if participant_1_id is not None and participant_2_id is not None:
            if participant_1_id > participant_2_id:
                self.participant_1, self.participant_2 = self.participant_2, self.participant_1

        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["participant_1", "participant_2"],
                name="unique_direct_conversations",
            )
        ]
        ordering = ["-created_at"]


class GroupConversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name="group_conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]


class DirectMessage(models.Model):
    conversation = models.ForeignKey(DirectConversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} - {self.content[:50]}"

    class Meta:
        ordering = ["-created_at"]


class GroupMessage(models.Model):
    conversation = models.ForeignKey(GroupConversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} - {self.content[:50]}"

    class Meta:
        ordering = ["-created_at"]
