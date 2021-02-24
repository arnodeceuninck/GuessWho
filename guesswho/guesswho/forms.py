from .models import PersonSet, Person
from django import forms
from django.forms import inlineformset_factory


class CreateDeckForm(forms.Form):
    name = forms.CharField(max_length=255)
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
# PersonFormSet = inlineformset_factory(PersonSet, Person, fields=('name',))
#
# class PersonSetForm(forms.ModelForm):
#     # name = forms.CharField(max_length=255)
#
#     class Meta:
#         model = PersonSet
#         fields = ['name']
#
#
# class PersonForm(forms.ModelForm):
#     # photo = forms.ImageField(label='image')
#     # name = forms.CharField(max_length=255)
#
#     class Meta:
#         model = Person
#         fields = ["photo", "name"]
