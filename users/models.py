from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_seller = models.BooleanField(default=False)
    # Add other common fields if needed, e.g.:
    # profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    # bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.username
