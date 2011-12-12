from django import forms
import json
from pymongo import json_util

class DocumentForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput, required=False)
    json = forms.CharField(widget=forms.Textarea(attrs={'class': 'xxlarge', 'rows': '4'}))

    def clean_json(self):
        try:
            return json.loads(self.cleaned_data['json'], object_hook=json_util.object_hook)
        except Exception, e:
            raise forms.ValidationError('Invalid JSON: %s' % unicode(e))
