from django.forms import ModelForm
import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class BookForm(forms.Form):
    Title = forms.CharField(max_length=255)
    upload_cover = forms.ImageField(max_length=255)
    upload_urls = forms.FileField(max_length=255)

    def clean(self):
        return True
        
    
