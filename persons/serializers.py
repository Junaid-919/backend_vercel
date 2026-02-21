from rest_framework import serializers
from persons.models import Person
from persons.models import Person, Location, BusService, BusStop, Bus

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class BusServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusService
        fields = "__all__"


class BusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bus
        fields = "__all__"



class ScheduleTwoTimesSerializer(serializers.Serializer):
    bus_stopno = serializers.IntegerField()
    bus_serviceno = serializers.IntegerField()
    arrival_time = serializers.IntegerField()
    next_arrival = serializers.IntegerField(allow_null=True)


class BusStopSerializer(serializers.ModelSerializer):
    bussservice = BusServiceSerializer(many=True, read_only=True)
    class Meta:
        model = BusStop
        fields = "__all__"
