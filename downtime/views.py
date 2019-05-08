# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from downtime.models import Downtime, Location, Alerts
from dal import autocomplete
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.models import User
from .forms import NewDowntimeForm
from utils.smsc_api import *
import pytz
import locale


DOWN_REASONS = {k: v for k, v in Downtime.REASONS}


local_tz = pytz.timezone('Europe/Moscow')
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)


@login_required(redirect_field_name='')
def index(request):

    form = NewDowntimeForm()

    return render(request, 'index.html', {'form': form})


@login_required(redirect_field_name='')
def get(request):

    data = {'data': get_all_downtimes()}

    return JsonResponse(data, safe=False)


def get_all_downtimes():

    times = Downtime.objects.values(
        'number',
        'location__name',
        'reason', 'comment',
        'starttime', 'finishtime',
        'status', 'id',
        'location__region', 'mass_error', 'com_a_close', 'created_by', 'closed_by'
    ).order_by('status', 'starttime').reverse()

    downtimes = []
    for line in times:
        user = User.objects.get(id=line['created_by']).username
        downtimes.append({"name": line['location__name'],
         "reasons": DOWN_REASONS[line['reason']],
         "number": line['number'],
         "comments": line['comment'],
         "startdate": line['starttime'].strftime('%H:%M - %d %B %Y'),
         "created_by": user,
         "region": line['location__region'],
         "mass_error": line['mass_error'],
         "id": line['id'],
         "status": line['status'],
         "com_a_close": line['com_a_close'],
         "finishdate": line['finishtime'].strftime('%H:%M - %d %B %Y') if line['finishtime'] is not None else '',
         "closed_by": line['closed_by'],
         })


    return downtimes


def get_active_downtimes():

    times = Downtime.objects.values(
        'location__name', 'starttime', 'finishtime',
        'reason', 'comment', 'ticket'
    ).filter(finishtime__isnull=True)

    downtimes = [
        {
            "name": line['location__name'],
            "reasons": DOWN_REASONS[line['reason']],
            "comments": line['comment'],
            "ticket": line['ticket'],
            "startdate": line['starttime']
        } for line in times]

    return downtimes


def get_active(request):

    data = {'date': get_active_downtimes()}

    return JsonResponse(data, safe=False)


@login_required(redirect_field_name='')
def add(request):

    if request.method == 'POST':
        form = NewDowntimeForm(request.POST)
        if form.is_valid():
            month = datetime.datetime.now().strftime('%m')
            year = datetime.datetime.now().strftime('%Y')
            count = Downtime.objects.filter(starttime__year=year, starttime__month=month).count() + 1

            count = '0'*(4-len(str(count))) + str(count)
            number = "%s_%s" % (month, count)
            downtime = Downtime.objects.create(
                number= number,
                location=Location.objects.get( name=form.cleaned_data['locations']),
                reason=form.cleaned_data.get('reason'),
                ticket=form.cleaned_data.get('ticket'),
                status=Downtime.DOWN_STATUS,
                comment=form.cleaned_data.get('comment'),
                mass_error=form.cleaned_data.get('massive'),
                created_by=User.objects.get(username=request.user.username),
                starttime=datetime.datetime.now()
            )
            try:
                sms_alert(
                    form.cleaned_data['locations'], form.cleaned_data.get('reason'),
                    form.cleaned_data.get('ticket'), mass_error=form.cleaned_data.get('massive')
                )
            except Exception as exp:
                print(exp)

            return redirect('/')

        else:
            return HttpResponse('Forms is not valid!!!!')


def sms_alert(location, reason, ticket, mass_error=False):
    receivers = [i.phone.encode('utf-8') for i in Alerts.objects.all() if i.send]

    if receivers:
        sms_text = '{}ТП \"{}\" поставлена на простой c {} по причине \"{}\". Номер тикета {}'.format(
            'МАССОВЫЙ СБОЙ! ' if mass_error else '',
            location, datetime.datetime.now().strftime('%I:%M - %d %B %Y'),
            DOWN_REASONS[reason], ticket).encode('utf-8')
        smsc = SMSC()
        smsc.send_sms(','.join(receivers), sms_text)
    else:
        pass


@login_required(redirect_field_name='')
def update(request):

    req = request.GET['id']
    stat = int(request.GET['status'])
    com = request.GET['com']
    times = Downtime.objects.get(id=req)
    times.finishtime = datetime.datetime.now()
    times.status = stat
    times.closed_by = request.user.username
    times.com_a_close = com
    times.save(update_fields=['finishtime', 'status', 'closed_by', 'com_a_close'])

    result = {
        "result": "success",
        "data": get_all_downtimes()
    }

    return JsonResponse(result)


class LocationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Location.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q.capitalize())

        return qs


def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('/')
            else:
                err_msg = u"Пользователь отключен. Обратитесь к администратору."
                return render(request, 'login.html', {'err_msg': err_msg})
        else:
            err_msg = u"Проверьте корректность логина/пароля."
            return render(request, 'login.html', {'err_msg': err_msg})
    else:
        return render(request, 'login.html')


@login_required(redirect_field_name='')
def logout(request):
    auth_logout(request)
    return redirect('/')
