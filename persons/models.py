from django.db import models

class Person(models.Model):
    name = models.TextField()
    age = models.TextField()
    phone = models.TextField()
    bloodgroup = models.TextField()
    address = models.TextField()

    def __str__(self):
        return self.name
