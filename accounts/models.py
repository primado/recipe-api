from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    headline = models.CharField("Headline", blank=True, max_length=150)
    instagram = models.URLField('Instagram Profile Link', blank=True)
    facebook = models.URLField("Facebook Profile Link", blank=True)
    website = models.URLField('Website Link', blank=True)
    profile_picture = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.username
    

