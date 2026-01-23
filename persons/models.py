from django.db import models

class Person(models.Model):
    name = models.TextField()
    age = models.TextField()
    phone = models.TextField()
    bloodgroup = models.TextField()
    address = models.TextField()

class Location(models.Model):
    latitude = models.TextField()
    longitude = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
