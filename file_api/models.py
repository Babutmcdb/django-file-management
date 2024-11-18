from django.db import models
from django.contrib.auth.models import User

class Entry(models.Model):
    TYPE_CHOICES = [
        ('folder', 'Folder'),
        ('file', 'File'),
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)  # 'folder' or 'file'
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to user
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'parent', 'owner')  # Unique name within the same folder for the same user

    def __str__(self):
        return f"{self.name} ({self.type})"
