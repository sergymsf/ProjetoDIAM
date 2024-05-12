from django.db import models
from django.contrib.auth.models import User

class ClothingItem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.FileField(default="")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.TextField(blank=True)

class Outfit(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    clothing_items = models.ManyToManyField(ClothingItem)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    favorite_clothing_item = models.OneToOneField(ClothingItem, related_name='favorited_by', blank=True, null=True, on_delete=models.SET_NULL)
    favorite_outfit = models.OneToOneField(Outfit, related_name='favorited_by', blank=True, null=True, on_delete=models.SET_NULL)