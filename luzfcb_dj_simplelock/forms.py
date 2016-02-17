# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms


class DeletarForm(forms.Form):

    def __init__(self, id_obj=None, *args, **kwargs):
        self._id = id_obj
        super(DeletarForm, self).__init__(*args, **kwargs)

    idd = forms.CharField(widget=forms.HiddenInput)
    hashe = forms.CharField(widget=forms.HiddenInput)

    def clean(self):
        idd = self.cleaned_data.get('idd')
        hashe = self.cleaned_data.get('hashe')
        if not self._id == idd and not idd == hashe:
            raise forms.ValidationError(
                "Hash errado"
            )


class ReValidarForm(forms.Form):

    def __init__(self, id_obj=None, *args, **kwargs):
        self._id = id_obj
        super(ReValidarForm, self).__init__(*args, **kwargs)

    idd = forms.CharField(widget=forms.HiddenInput)
    hashe = forms.CharField(widget=forms.HiddenInput)

    def clean(self):
        idd = self.cleaned_data.get('idd')
        hashe = self.cleaned_data.get('hashe')
        if not self._id == idd and not idd == hashe:
            raise forms.ValidationError(
                "Hash errado"
            )
