from django import forms
from django.forms import ModelForm
from .models import UserProfile


class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'id': 'loginUsername',
                'type': 'text',
                'class': 'form-control'
            }
        ))

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'loginPassword',
            'type': 'password',
            'class': 'form-control',
        })
    )


class UserSignUpForm(forms.Form):
    profile_pic = forms.ImageField(
        widget=forms.FileInput(
            attrs={'class': 'form-control-file'}
        ))

    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control'
            }
        ))

    CHOICES = (('', 'Seleccionar'), ('2', 'Vendedor'), ('3', 'Comprador'),)
    id_rol = forms.ChoiceField(choices=CHOICES,
                               widget=forms.Select(
                                   attrs={
                                       'class': 'form-select'
                                   }))

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'id': 'signupEmail',
                'type': 'email',
                'class': 'form-control'
            }
        )
    )

    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control'
            }
        ))

    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control'
            }
        ))

    phone = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control'
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'id': 'signupPassword',
                'type': 'password',
                'class': 'form-control'
            }
        ))

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'class': 'form-control'
            }
        ))

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Las Contraseñas no coinciden')
        return cd['password2']


class UserEditProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = UserProfile
        fields = 'profile_pic', 'email', 'first_name', 'last_name', 'phone',
        widgets = {
            'profile_pic': forms.FileInput(
                attrs={
                    'class': 'form-control-file',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'id': 'signupEmail',
                    'class': 'form-control'
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'groups',
                   'username', 'password']

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
