from django.db import models

class Person(models.Model):
    name = models.TextField()
    age = models.TextField()
    phone = models.TextField()
    bloodgroup = models.TextField()
    address = models.TextField()