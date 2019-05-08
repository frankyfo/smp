# coding: utf8
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    id = models.IntegerField(verbose_name="Номер точки", primary_key=True)
    name = models.CharField(verbose_name="Название", max_length=100)
    region = models.CharField(verbose_name="Регион", max_length=50)
    ip = models.CharField(verbose_name="IP", max_length=15, default="")

    def __str__(self):
        return self.name


class Downtime(models.Model):
    DOWN_FINISH = 1
    DOWN_STATUS = 2
    DOWN_UNKNOWN = 3
    DOWN_MISTAKE = 0

    STATUSES = (
        (DOWN_STATUS, u'Простой'),
        (DOWN_FINISH, u'Простой завершен'),
        (DOWN_UNKNOWN, u'Неизвестен'),
        (DOWN_MISTAKE, u'Ошибочный'),
    )

    RESULT_INET = "I"
    RESULT_PRINTER = "M"
    RESULT_ELECTRIK = "E"
    RESULT_PO_ERROR = "P"
    RESULT_NOT_EMPLOYEE = "L"
    RESULT_OTHER = "T"

    REASONS = (
        (RESULT_INET, u'Нет интернета'),
        (RESULT_PRINTER, u'Не работает МФУ'),
        (RESULT_ELECTRIK, u'Нет электричества'),
        (RESULT_PO_ERROR, u'Не работает ПО'),
        (RESULT_NOT_EMPLOYEE, u'Нет сотрудников'),
        (RESULT_OTHER, u'Прочее в комментарии'),
    )

    number = models.CharField(verbose_name=u"Номер простоя", max_length=12, default='без номера')
    starttime = models.DateTimeField(verbose_name=u"Начало простоя")
    finishtime = models.DateTimeField(verbose_name=u"Конец простоя", null=True, blank=True)
    status = models.CharField(verbose_name=u"Статус", choices=STATUSES, max_length=1, default=DOWN_UNKNOWN)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    reason = models.CharField(verbose_name=u"Причина", choices=REASONS, max_length=1, default=RESULT_INET)
    comment = models.CharField(max_length=200, verbose_name=u"Комментарий", null=True, blank=True)
    com_a_close = models.CharField(max_length=200, verbose_name=u"Комментарий по закрытию", null=True, blank=True)
    ticket = models.CharField(max_length=15, verbose_name=u"Номер тикета", null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name=u"Пользователь открыл")
    closed_by = models.CharField(max_length=200, verbose_name=u"Пользователь закрыл", null=True, blank=True)
    mass_error = models.BooleanField(default=False)

    def __str__(self):
        return u"%s %s" % (self.location, self.starttime)


class Alerts(models.Model):
    name = models.CharField(verbose_name="ФИО", max_length=50)
    phone = models.CharField(verbose_name="Номер телефона", max_length=11)
    send = models.BooleanField(default=False)

    def __str__(self):
        return u"%s" % (self.name)
