from django import forms
import json
from bson import json_util

from . import models


class ConnectForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    class Meta:
        model = models.MongoConnection
        fields = ['name', 'host', 'port','auth_database', 'username', 'password', 'database']


class CollectionFilterForm(forms.Form):
    page = forms.IntegerField(required=False)
    query = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'xxlarge', 'rows': '1'}))
    fields = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'xxlarge', 'rows': '1'}))

    def clean_fields(self):
        if self.cleaned_data['fields']:
            try:
                return json.loads(self.cleaned_data['fields'], object_hook=json_util.object_hook)
            except Exception as e:
                raise forms.ValidationError('Invalid JSON: %s' % e)

    def clean_query(self):
        if self.cleaned_data['query']:
            try:
                return json.loads(self.cleaned_data['query'], object_hook=json_util.object_hook)
            except Exception as e:
                raise forms.ValidationError('Invalid JSON: %s' % e)


class DocumentForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput, required=False)
    json = forms.CharField(widget=forms.Textarea(attrs={'class': 'xxlarge', 'rows': '4'}))

    def clean_json(self):
        try:
            return json.loads(self.cleaned_data['json'], object_hook=json_util.object_hook)
        except Exception as e:
            raise forms.ValidationError('Invalid JSON: %s' % e)
