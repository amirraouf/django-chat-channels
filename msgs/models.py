from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.utils import timezone


class Message(models.Model):
    text = models.TextField()
    room = models.ForeignKey('msgs.Room', on_delete=models.CASCADE)
    from_user = models.OneToOneField(User)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)


class Room(models.Model):
    name = models.CharField(max_length=265, blank=True)
    from_user = models.ForeignKey(User, related_name='from_user', null=True)
    to_user = models.ForeignKey(User, related_name='to_user', null=True)

    def __str__(self):
        return "%s-%s".format(self.from_user.first_name, self.to_user.first_name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.name = self.__str__()
        self.save()

