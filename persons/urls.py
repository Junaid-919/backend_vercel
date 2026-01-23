from django.urls import path
from . import views  # import the module itself

urlpatterns = [
    path("get_person_data/", views.get_person_data, name="get_person_data"),
    path("create_person_data/", views.create_person_data, name="create_person_data"),
    path("update_person/<int:person_id>/", views.update_person, name="update_person"),
    path("delete_person/<int:person_id>/", views.delete_person, name="delete_person"),
    path("get_person_withid/<int:person_id>/", views.get_person_withid, name="get_person_withid"),
<<<<<<< HEAD
]
=======



    path("get_location_data/", views.get_location_data, name="get_location_data"),
    path("create_location_data/", views.create_location_data, name="create_person_data"),
    path("update_location/<int:location_id>/", views.update_location, name="update_person"),
    path("delete_location/<int:location_id>/", views.delete_location, name="delete_person"),
    path("get_location_withid/<int:location_id>/", views.get_location_withid, name="get_person_withid"),
]
>>>>>>> 47c1e98 (Initial commit jan23)
