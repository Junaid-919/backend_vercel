from rest_framework import serializers
<<<<<<< HEAD
from persons.models import Person
=======
from persons.models import Person, Location
>>>>>>> 47c1e98 (Initial commit jan23)

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"
<<<<<<< HEAD
=======


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
>>>>>>> 47c1e98 (Initial commit jan23)
