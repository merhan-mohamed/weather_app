from django.urls import path
from .views import weather, delete_city

app_name = 'Weather'

urlpatterns = [
    path('weather', weather, name='weather'),
    path('delete_city/<str:city_name>/',delete_city,name='delete_city')
    ]