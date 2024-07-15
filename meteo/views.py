from datetime import datetime

import geocoder
import requests
from django.http import HttpResponse
from django.template import loader
from meteo.models import Worldcities


# Create your views here.
def temp_somewhere(request):
    random_item = Worldcities.objects.all().order_by('?').first()
    city = random_item.city
    country = random_item.country
    location = [random_item.lat, random_item.lng]
    temp = get_temp(location)
    template = loader.get_template("index.html")
    context = {
        "country": country,
        "city": city,
        "temp": temp
    }
    return HttpResponse(template.render(context, request))


def temp_here(request):
    location = geocoder.ip('me').latlng
    g = geocoder.ip('me')
    city = g.city
    country = g.country
    temp = get_temp(location)
    template = loader.get_template("index.html")
    context = {
        "country": country if country else "",
        "city": city if city else "Your location",
        "temp": temp
    }
    return HttpResponse(template.render(context, request))


def get_temp(location):
    endpoint = "https://api.open-meteo.com/v1/forecast"
    lat = location[0]
    lon = location[1]
    api_request = f"{endpoint}?latitude={lat}&longitude={lon}&hourly=temperature_2m"
    now = datetime.now()
    hour = now.hour
    meteo_data = requests.get(api_request).json()
    temp = meteo_data['hourly']['temperature_2m'][hour]
    return temp
