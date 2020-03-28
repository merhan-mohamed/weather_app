from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import City
from .forms import CityForm
import requests

# Create your views here.
def weather(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=9de243494c0b295cca9337e1e96b00e2'

    err_message =''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_message = 'City does not exist in the world'
            else :
                err_message = 'City already exists in the database'
        if err_message:
            message = err_message
            message_class = 'is-danger'
        else:
            message = 'City added successfully'
            message_class = 'is-success'


    form = CityForm()
    cities = City.objects.all()
    weather_data =[]
    for city in cities:
        response = requests.get(url.format(city)).json()
        city_weather = {
            'city': city,
            'temperature': response['main']['temp'],
            'description': response['weather'][0]['description'],
            'icon':response['weather'][0]['icon'],
        }
        weather_data.append(city_weather)
    context = {
        'weather_data' :  weather_data,
        'form': form,
        'message': message,
        'message_class': message_class
    }
    return render(request, 'weather.html',context)

def delete_city(request,city_name):
    City.objects.get(name=city_name).delete()
    return redirect('Weather:weather')



