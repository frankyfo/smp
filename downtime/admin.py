from django.contrib import admin
from downtime import models


# Register your models here.
admin.site.register(models.Location)
admin.site.register(models.Downtime)
admin.site.register(models.Alerts)
