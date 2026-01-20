from django.urls import path
from .views import get_person_data, create_person_data, update_person, delete_person, get_person_withid

urlpatterns = [
    path('api/get_person_data/', views.get_person_data, name='get_person_data'),
    path('api/create_person_data/', views.create_person_data, name='create_person_data'),
    path('api/update_person/<int:person_id>/', views.update_person, name='update_person'),
    path('api/delete_person/<int:person_id>/', views.delete_person, name='delete_person'),
    path('api/get_person_withid/<int:person_id>/', views.get_person_withid, name='get_person_withid'),
]