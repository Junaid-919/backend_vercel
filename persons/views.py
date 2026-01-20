from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models.persons import Person
from ..serializers.person_serializers import PersonSerializer

@api_view(['GET'])
def get_person_data(request):
    try:
        Rohit = Person.objects.all()
        serializer = PersonSerializer(Rohit, many=True)
        return Response(serializer.data)
    except Person.DoesNotExist:  # corrected 'execpt' to 'except'
        return Response({"error": "Person not found."}, status=404)


@api_view(['POST'])
def create_person_data(request):
    try:
        request_data = request.data.copy()
        serializer = PersonSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

    except Person.DoesNotExist:  # corrected 'execpt' to 'except'
        return Response({"error": "Person not found."}, status=400)

@api_view(['PUT'])
def update_person(request, person_id):
    try:
        person = Person.objects.get(id=person_id)
        serializer = PersonSerializer(person,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
    except Person.DoesNotExist:  # corrected 'execpt' to 'except'
        return Response({"error": "Person not found."}, status=404)

@api_view(['DELETE'])
def delete_person(request, person_id):
    try:
        person = Person.objects.get(id=person_id)
        person.delete()
        return Response({"message": "Person deleted successfully."},status=204)
    except Person.DoesNotExist:  # corrected 'execpt' to 'except'
        return Response({"error": "Person not found."}, status=404)
        


@api_view(['GET'])
def get_person_withid(request, person_id):
    try:
        person = Person.objects.get(id=Pprson_id)
        serializer = person_serializer(person,partial=True)
        return Response(serializer.data)
    except Person.DoesNotExist:  # corrected 'execpt' to 'except'
        return Response({"error": "Person not found."}, status=404)