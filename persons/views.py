# persons/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from persons.models import Person
from persons.serializers import PersonSerializer
from persons.models import Person, Location
from persons.serializers import PersonSerializer, LocationSerializer



@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})

@api_view(['GET'])
def get_person_data(request):
    persons = Person.objects.all()
    serializer = PersonSerializer(persons, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_person_data(request):
    serializer = PersonSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def update_person(request, person_id):
    try:
        person = Person.objects.get(id=person_id)
    except Person.DoesNotExist:
        return Response({"error": "Person not found"}, status=404)

    serializer = PersonSerializer(person, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_person(request, person_id):
    try:
        person = Person.objects.get(id=person_id)
    except Person.DoesNotExist:
        return Response({"error": "Person not found"}, status=404)

    person.delete()
    return Response(status=204)

@api_view(['GET'])
def get_person_withid(request, person_id):
    try:
        person = Person.objects.get(id=person_id)
    except Person.DoesNotExist:
        return Response({"error": "Person not found"}, status=404)

    serializer = PersonSerializer(person)
    return Response(serializer.data)

# ========================================================


@api_view(['GET'])
def get_location_data(request):
    persons = Location.objects.all()
    serializer = LocationSerializer(persons, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_location_data(request):
    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def update_location(request, location_id):
    try:
        person = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        return Response({"error": "Location not found"}, status=404)

    serializer = LocationSerializer(person, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_location(request, location_id):
    try:
        person = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        return Response({"error": "Location not found"}, status=404)

    person.delete()
    return Response(status=204)

@api_view(['GET'])
def get_location_withid(request, location_id):
    try:
        person = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        return Response({"error": "Location not found"}, status=404)

    serializer = LocationSerializer(person)
    return Response(serializer.data)
