from django import forms
from users.models import UserProfile

from .models import Category


class CreateProductForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'id': 'title',
                'type': 'text',
                'class': 'form-control'
            }
        ))
    image = forms.ImageField(
        widget=forms.FileInput(
            attrs={'class': 'form-control-file'}
        ))
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        ))
    price = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ))

    id_category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                         widget=forms.Select(
                                             attrs={
                                                 'class': 'form-select'
                                             }))

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                u = form.save(commit=False)
                u.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
