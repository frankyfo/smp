import requests
from django.conf import settings
from downtime.models import Location
#from main.celery import app

#@app.task
def sync_locations():
    r = requests.get("http://" + settings.ITAPP_URL + '/tplist/get_location_list')
    data = r.json()
    for v in data:
        if not Location.objects.filter(name=v['name']).exists():
            Location.objects.create(
                 id=len(Location.objects.all()) +1,
                 name=v['name'],
                 region=v['city__cityName']
            )