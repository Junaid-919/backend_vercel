from rest_framework.decorators import api_view
from rest_framework.response import Response
from persons.models import Person
from persons.serializers import PersonSerializer


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
