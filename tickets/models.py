from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

from django.contrib.auth.models import User
# Create your models here.
#guest -- movie -- reservation

class Movie(models.Model):
    hall = models.CharField(max_length=100)
    movie = models.CharField(max_length=100)
    # time = models.CharField(max_length=100)

class Guest(models.Model):
    name =models.CharField(max_length=100)
    mobile =models.CharField(max_length=100)

class Reservation(models.Model):
    guest = models.ForeignKey(Guest, related_name='reservations', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='reservations', on_delete=models.CASCADE)



class Post(models.Model):
    auther= models.ForeignKey(User , on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()



# create token for each user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


