# -*- coding: utf-8 -*-
from django import forms
from .models import Downtime, Location
from dal import autocomplete


class NewDowntimeForm(forms.Form):

    location = Location.objects.all()

    locations = forms.ModelChoiceField(
        label='Выбор ТП',
        queryset=location,
        widget=autocomplete.ModelSelect2(url='location-autocomplete')
    )

    reason = forms.ChoiceField(
        label='Причина', choices=Downtime.REASONS,
        widget=forms.Select(attrs={'id': 'disabledSelect', 'class': 'form-control'})
    )

    comment = forms.CharField(
        label='Комментарий',
        widget=forms.Textarea(
            attrs={'rows': 8, 'placeholder': 'Введите дополнительную информацию', 'class': 'form-control noresize'}),
        max_length=200, empty_value='-', required=False
    )

    massive = forms.BooleanField(
        label='Массовый сбой', required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check'})
    )
