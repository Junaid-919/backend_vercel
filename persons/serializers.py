from rest_framework import serializers
from persons.models import Person
from persons.models import Person, Location, BusService, BusStop

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class BusStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStop
        fields = "__all__"


class BusServiceSerializer(serializers.ModelSerializer):
    busstop = serializers.PrimaryKeyRelatedField(queryset=BusStop.objects.all())

    class Meta:
        model = BusService
        fields = "__all__"

        
    def to_representation(self, instance):
        """
        Customize representation to include detailed patient information.
        """
        representation = super().to_representation(instance)
        # Replace `patient` ID with full serialized data
        representation['busstop'] = BusStopSerializer(instance.busstop).data
        return representation
