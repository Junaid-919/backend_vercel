# persons/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta, datetime, date
import random

from django.db.models import Window, F
from django.db.models.functions import RowNumber, Lead

from persons.models import Person, Location, BusStop, BusService, Bus
from persons.serializers import (
    PersonSerializer,
    LocationSerializer,
    BusStopSerializer,
    BusServiceSerializer,
    BusSerializer,
)
from rest_framework.views import APIView

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
        busstop = BusStop.objects.prefetch_related('bussservice').get(bus_stop_number=bus_stop_number)
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

#  ==============================================================

@api_view(['POST'])
def post_bus_data(request):
    serializer = BusSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def get_bus_data(request):
    qs = Bus.objects.all()
    serializer = BusServiceSerializer(qs, many=True)
    return Response(serializer.data)





@api_view(['GET'])
def get_arr(request, pk):
    current_time = datetime.now().time()

    print("curect time = ", current_time)

    # Get next 2 schedules
    schedules = list(
        Bus.objects
        .filter(bus_stopno=pk, arrival_time__gt=current_time)
        .order_by('arrival_time')[:2]
    )

    schedules1 = list(
        Bus.objects
        .filter(bus_stopno=pk, arrival_time__gt=current_time)
        .order_by('arrival_time').values()[:2]
    )

    print("shedules = ", schedules1)

    if not schedules:
        return Response({"message": "No upcoming times found"})

    first = schedules[0]
    second = schedules[1] if len(schedules) > 1 else None

    print("first = ", first)
    print("second = ", second)

    data = [{
        "bus_stopno": first.bus_stopno,
        "bus_serviceno": first.bus_serviceno,
        "arrival_time": first.arrival_time.strftime("%H:%M:%S"),
        "next_time": second.arrival_time.strftime("%H:%M:%S") if second else None
    }]

    return Response(data)



from .serializers import ScheduleTwoTimesSerializer
from rest_framework.views import APIView


class ScheduleByRegisterView(APIView):

    def get(self, request, pk):
        current_time = datetime.now().time()
        current_datetime = timezone.localtime()
        current_time = current_datetime.time()


        queryset1 = (
            Bus.objects
            .filter(bus_stopno=pk, arrival_time__gt=current_time)
            .annotate(
                row_number=Window(
                    expression=RowNumber(),
                    partition_by=[F('bus_serviceno')],
                    order_by=F('arrival_time').asc()
                ),
                next_arrival=Window(
                    expression=Lead('arrival_time'),
                    partition_by=[F('bus_serviceno')],
                    order_by=F('arrival_time').asc()
                )
            )
            .filter(row_number=1)  # Only first record per subregisterno
            .values(
                'bus_stopno',
                'bus_serviceno',
                'arrival_time',
                'next_arrival'
            )
            .order_by('bus_serviceno').values()
        )

        print("current time = ", current_time)
        print("objects = ", queryset1)

        queryset = (
            Bus.objects
            .filter(bus_stopno=pk, arrival_time__gt=current_time)
            .annotate(
                row_number=Window(
                    expression=RowNumber(),
                    partition_by=[F('bus_serviceno')],
                    order_by=F('arrival_time').asc()
                ),
                next_arrival=Window(
                    expression=Lead('arrival_time'),
                    partition_by=[F('bus_serviceno')],
                    order_by=F('arrival_time').asc()
                )
            )
            .filter(row_number=1)  # Only first record per subregisterno
            .values(
                'bus_stopno',
                'bus_serviceno',
                'arrival_time',
                'next_arrival'
            )
            .order_by('bus_serviceno')
        )


        result = []

        for obj in queryset:

            # Convert schedule_time to datetime (today)
            schedule_dt = datetime.combine(date.today(), obj['arrival_time'])
            schedule_dt = timezone.make_aware(schedule_dt)

            # Calculate difference in minutes
            diff_minutes = int((schedule_dt - current_datetime).total_seconds() / 60)

            next_diff_minutes = None
            if obj['next_arrival']:
                next_dt = datetime.combine(date.today(), obj['next_arrival'])
                next_dt = timezone.make_aware(next_dt)
                next_diff_minutes = int((next_dt - current_datetime).total_seconds() / 60)

            result.append({
                "bus_stopno": obj["bus_stopno"],
                "bus_serviceno": obj["bus_serviceno"],
                "arrival_time": diff_minutes,
                "next_arrival": next_diff_minutes
            })

        serializer = ScheduleTwoTimesSerializer(result, many=True)
        return Response(serializer.data)



class RegisterScheduleView(APIView):

    def get(self, request, pk):

        # Get register object
        try:
            busstop = BusStop.objects.get(bus_stop_number=pk)
        except BusStop.DoesNotExist:
            return Response({"error": "BusStop not found"}, status=404)

        # Get current time (IST if configured)
        current_time = timezone.localtime().time()

        # Get next schedule + next_schedule per subregisterno
        schedules = (
            Bus.objects
            .filter(
                busstop=busstop,
                arrival_time__gt=current_time
            )
            .annotate(
                row_number=Window(
                    expression=RowNumber(),
                    partition_by=[F('bus_serviceno')],
                    order_by=F('arrival_time').asc()
                ),
                next_arrival=Window(
                    expression=Lead('arrival_time'),
                    partition_by=[F('bus_serviceno')],
                    order_by=F('arrival_time').asc()
                )
            )
            .filter(row_number=1)
            .values(
                'bus_serviceno',
                'arrival_time',
                'next_arrival'
            )
            .order_by('bus_serviceno')
        )

        response_data = {
            "current_time": datetime.now().time(),
            "bus_stop_number": busstop.bus_stop_number,
            "bus_stop_name": busstop.bus_stop_name,
            "bus_details": list(schedules)
        }

        return Response(response_data)