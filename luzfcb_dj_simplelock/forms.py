from django import forms


class DeletarForm(forms.Form):
    def __init__(self, id_obj=None, *args, **kwargs):
        self._id = id_obj
        super().__init__(*args, **kwargs)

    id = forms.CharField(widget=forms.HiddenInput)
    hash = forms.CharField(widget=forms.HiddenInput)

    def clean(self):
        id = self.cleaned_data.get('id')
        hash = self.cleaned_data.get('hash')
        if not self._id == id and not id == hash:
            raise forms.ValidationError(
                "Hash errado"
            )


class ReValidarForm(forms.Form):
    def __init__(self, id_obj=None, *args, **kwargs):
        self._id = id_obj
        super().__init__(*args, **kwargs)

    id = forms.CharField(widget=forms.HiddenInput)
    hash = forms.CharField(widget=forms.HiddenInput)

    def clean(self):
        id = self.cleaned_data.get('id')
        hash = self.cleaned_data.get('hash')
        if not self._id == id and not id == hash:
            raise forms.ValidationError(
                "Hash errado"
            )
