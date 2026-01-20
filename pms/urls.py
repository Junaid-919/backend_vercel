from django.contrib import admin
from django.urls import path, include
from persons.views import health

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("persons.urls")),
    path("", health),

]
