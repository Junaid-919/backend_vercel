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


class BusStop(models.Model):
    bus_stop_number = models.TextField()
    bus_stop_name = models.TextField()


class BusService(models.Model):
    busstop = models.ForeignKey(BusStop, on_delete=models.CASCADE,related_name='bussservice')
    service_number = models.TextField()
    arrival_time = models.DateTimeField()
    next_arrival_time = models.DateTimeField()
