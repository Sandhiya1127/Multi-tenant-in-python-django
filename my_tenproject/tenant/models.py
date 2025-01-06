# # tenant/models.py

from django.db import models
from shared.models import User

class TenantUserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    details = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s details"