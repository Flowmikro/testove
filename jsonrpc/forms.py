from django import forms


class JsonRpcForm(forms.Form):
    method = forms.CharField(label='Method', max_length=100)
    params = forms.JSONField(label='Params', required=False)
