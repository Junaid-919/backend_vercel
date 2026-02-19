# persons/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from persons.models import Person
from persons.serializers import PersonSerializer, BusStopSerializer, BusServiceSerializer
from persons.models import Person, Location, BusStop, BusService
from persons.serializers import PersonSerializer, LocationSerializer
from django.shortcuts import get_object_or_404
import random
from datetime import timedelta
from django.utils import timezone





@api_view(['GET'])
def busstop_detail1(request, bus_stop_number):
    try:
        try:
            person = BusStop.objects.get(bus_stop_number=bus_stop_number)
        except Person.DoesNotExist:
            return Response({"error": "Person not found"}, status=404)
        
        services = BusService.objects.filter(busstop=person)
        serializer = BusServiceSerializer(services, many=True)
        return Response(serializer.data)


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


# ========================================================
@api_view(['GET', 'POST'])
def busstop_collection(request):
    if request.method == 'GET':
        qs = BusStop.objects.all()
        serializer = BusStopSerializer(qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BusStopSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=201
            )
        return Response(serializer.errors, status=400)


@api_view(['PUT', 'PATCH'])
def busstop_detail(request, pk):
    """
    PUT/PATCH:  Update the bus stop identified by pk.
    """
    try:
        busstop = BusStop.objects.get(pk=pk)
    except BusStop.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=404)

    if request.method in ['PUT', 'PATCH']:
        serializer = BusStopSerializer(busstop, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

# ------------------------------------------------------------------
#  BusService
# ------------------------------------------------------------------

@api_view(['GET', 'POST'])
def busservice_collection(request):
    """
    GET:   List all bus services.
    POST:  Create a new bus service.
    """
    if request.method == 'GET':
        qs = BusService.objects.select_related('busstop').all()
        serializer = BusServiceSerializer(qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BusServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=201
            )
        return Response(serializer.errors, status=400)


@api_view(['PUT', 'PATCH'])
# @csrf_exempt                     # ← Uncomment if you truly want to skip CSRF
def busservice_detail(request, pk):
    """
    PUT/PATCH:  Update the bus service identified by pk.
    The arrival_time & next_arrival_time are automatically set to a random
    offset (0‑10 min) from now, with next_arrival_time always 5 min after that.
    """
    try:
        busservice = BusService.objects.get(pk=pk)
    except BusService.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=404)

    if request.method in ['PUT', 'PATCH']:
        # 1️⃣  Compute new times
        now = timezone.now()
        random_minute_offset = random.randint(0, 10)
        new_arrival = now + timedelta(minutes=random_minute_offset)
        new_next = new_arrival + timedelta(minutes=5)

        # 2️⃣  Ensure those values are present in the payload
        #       (they may already be sent by the client – we just override them)
        data = request.data.copy()
        data['arrival_time'] = new_arrival
        data['next_arrival_time'] = new_next

        # 3️⃣  Validate & save
        serializer = BusServiceSerializer(
            busservice, data=data, partial=(request.method == 'PATCH')
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
