from django.urls import path
from . import views  # import the module itself

urlpatterns = [
    path("get_person_data/", views.get_person_data, name="get_person_data"),
    path("create_person_data/", views.create_person_data, name="create_person_data"),
    path("update_person/<int:person_id>/", views.update_person, name="update_person"),
    path("delete_person/<int:person_id>/", views.delete_person, name="delete_person"),
    path("get_person_withid/<int:person_id>/", views.get_person_withid, name="get_person_withid"),
]
