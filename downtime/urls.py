"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from downtime import views
from downtime.views import LocationAutocomplete


urlpatterns = [
    url(r'^$', views.index),
    url(r'^get/', views.get),
    url(r'^add/', views.add),
    url(r'^update/', views.update),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^downtimes/', views.get_active),
    url(r'^location-autocomplete/$', LocationAutocomplete.as_view(), name='location-autocomplete')
]
