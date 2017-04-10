from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Message(models.Model):
    text = models.TextField()
    room = models.ForeignKey('msgs.Room', on_delete=models.CASCADE)
    from_user = models.OneToOneField(User)


class Room(models.Model):
    from_user = models.OneToOneField(User, related_name='from_user')
    to_user = models.OneToOneField(User, related_name='to_user')


class LoggedIn(models.Model):
    user = models.OneToOneField(User)