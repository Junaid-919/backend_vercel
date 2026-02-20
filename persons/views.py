# persons/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
import random

from persons.models import Person, Location, BusStop, BusService
from persons.serializers import (
    PersonSerializer,
    LocationSerializer,
    BusStopSerializer,
    BusServiceSerializer,
)

# ========================================================
# Health Check
# ========================================================

@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})


# ========================================================
# Person APIs
# ========================================================

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
# Location APIs
# ========================================================

@api_view(['GET'])
def get_location_data(request):
    locations = Location.objects.all()
    serializer = LocationSerializer(locations, many=True)
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
        location = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        return Response({"error": "Location not found"}, status=404)

    serializer = LocationSerializer(location, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def delete_location(request, location_id):
    try:
        location = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        return Response({"error": "Location not found"}, status=404)

    location.delete()
    return Response(status=204)


@api_view(['GET'])
def get_location_withid(request, location_id):
    try:
        location = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        return Response({"error": "Location not found"}, status=404)

    serializer = LocationSerializer(location)
    return Response(serializer.data)


# ========================================================
# BusStop APIs
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
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['PUT', 'PATCH'])
def busstop_detail(request, pk):

    try:
        busstop = BusStop.objects.get(pk=pk)
    except BusStop.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=404)

    serializer = BusStopSerializer(
        busstop,
        data=request.data,
        partial=(request.method == 'PATCH')
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


# 🔹 Get Bus Services by Bus Stop Number (GET only)
@api_view(['GET'])
def busstop_services_by_number(request, bus_stop_number):
    print("busstop method is called", bus_stop_number)
    try:
        # busstop = BusStop.objects.get(bus_stop_number=bus_stop_number)
        busstop = BusStop.objects.prefetch_related('busservice').get(bus_stop_number=bus_stop_number)
        print("busstop method is called line 186 ", bus_stop_number)
    except BusStop.DoesNotExist:
        return Response({"error": "Bus stop not found"}, status=404)

    serializer = BusStopSerializer(busstop)
    print("busstop method is called line 192 ", serializer.data)
    return Response(serializer.data)


# ========================================================
# BusService APIs
# ========================================================

@api_view(['GET', 'POST'])
def busservice_collection(request):

    if request.method == 'GET':
        qs = BusService.objects.select_related('busstop').all()
        serializer = BusServiceSerializer(qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BusServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['PUT', 'PATCH'])
def busservice_detail(request, pk):

    try:
        busservice = BusService.objects.get(pk=pk)
    except BusService.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=404)

    # Auto update times
    now = timezone.now()
    random_offset = random.randint(0, 10)
    new_arrival = now + timedelta(minutes=random_offset)
    new_next = new_arrival + timedelta(minutes=5)

    data = request.data.copy()
    data['arrival_time'] = new_arrival
    data['next_arrival_time'] = new_next

    serializer = BusServiceSerializer(
        busservice,
        data=data,
        partial=(request.method == 'PATCH')
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)
