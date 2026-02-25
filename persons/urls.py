from django.urls import path
from . import views  # import the module itself
from .views import ScheduleByRegisterView
from .views import RegisterScheduleView


urlpatterns = [
    path("get_person_data/", views.get_person_data, name="get_person_data"),
    path("create_person_data/", views.create_person_data, name="create_person_data"),
    path("update_person/<int:person_id>/", views.update_person, name="update_person"),
    path("delete_person/<int:person_id>/", views.delete_person, name="delete_person"),
    path("get_person_withid/<int:person_id>/", views.get_person_withid, name="get_person_withid"),

    path("get_location_data/", views.get_location_data, name="get_location_data"),
    path("create_location_data/", views.create_location_data, name="create_person_data"),
    path("update_location/<int:location_id>/", views.update_location, name="update_person"),
    path("delete_location/<int:location_id>/", views.delete_location, name="delete_person"),
    path("get_location_withid/<int:location_id>/", views.get_location_withid, name="get_person_withid"),


    path('busstops/', views.busstop_collection, name='busstop-list-create'),
    path('busstops/<int:pk>/', views.busstop_detail, name='busstop-detail'),

    # BusService
    path('busservices/', views.busservice_collection, name='busservice-list-create'),
    path('busservices/<int:pk>/', views.busservice_detail, name='busservice-detail'),
    path('busstops/number/<str:bus_stop_number>/', views.busstop_services_by_number),
    path('busstops/arr/<str:pk>/', views.get_arr),
    path('busstops/arr1/<str:pk>/', ScheduleByRegisterView.as_view()),
    path("tracker/<str:pk>/", RegisterScheduleView.as_view()),

]
