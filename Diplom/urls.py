from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('Latrello.urls')),
    path('api/', include('Latrello.api.urls')),

]
