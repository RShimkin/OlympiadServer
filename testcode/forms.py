from django import forms
# from django.core.exceptions import ValidationError

from .models import *

class CodeForm(forms.Form):
    title = forms.CharField(max_length=255)
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 120, 'rows': 17, 'class':'form-control', 'id':'ta', 'required': False}))
    plang = forms.ChoiceField(choices = LANG_CHOICES)

class MyCodeForm(forms.Form):
    title = forms.CharField(max_length=255)
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 120, 'rows': 17, 'class':'form-control', 'id':'ta', 'required': False}))
    plang = forms.ChoiceField(choices = LANG_CHOICES)

