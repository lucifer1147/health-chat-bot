from django.db import models
from django.utils import timezone


class Room(models.Model):
    name = models.CharField(max_length=1000)


class Message(models.Model):
    value = models.CharField(max_length=10000)
    date = models.DateTimeField(default=timezone.now, blank=True)
    user = models.CharField(max_length=100)
    room = models.CharField(max_length=100)
