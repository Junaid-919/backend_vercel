from django.urls import path
from . import views

urlpatterns = [
    path("get_person_data/", views.get_person_data),
    path("create_person_data/", views.create_person_data),
    path("update_person/<int:person_id>/", views.update_person),
    path("delete_person/<int:person_id>/", views.delete_person),
    path("get_person_withid/<int:person_id>/", views.get_person_withid),
]
