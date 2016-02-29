# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

# TODO: Incluir geracao do hash para verificacao se pode ou nao revalidar o bloqueio

class DeleteForm(forms.Form):

    def __init__(self, id_obj=None, *args, **kwargs):
        self._id = id_obj
        super(DeleteForm, self).__init__(*args, **kwargs)

    idd = forms.CharField(widget=forms.HiddenInput)
    hashe = forms.CharField(widget=forms.HiddenInput)

    def clean(self):
        idd = self.cleaned_data.get('idd')
        hashe = self.cleaned_data.get('hashe')
        if not self._id == idd and not idd == hashe:
            raise forms.ValidationError(
                "Hash errado"
            )


class ReValidateForm(forms.Form):

    def __init__(self, id_obj=None, *args, **kwargs):
        self._id = id_obj
        super(ReValidateForm, self).__init__(*args, **kwargs)

    idd = forms.CharField(widget=forms.HiddenInput)
    hashe = forms.CharField(widget=forms.HiddenInput)

    def clean(self):
        idd = self.cleaned_data.get('idd')
        hashe = self.cleaned_data.get('hashe')
        if not self._id == idd and not idd == hashe:
            raise forms.ValidationError(
                "Hash errado"
            )
