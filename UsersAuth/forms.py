from UsersAuth.models import Account
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import datetime


class RegisterForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['username', 'email', 'first_name', 'last_name','birth', 'health_id','password1', 'password2','profile_pic','phone']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'First name *'
            }),
            'last_name': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Last name *'
            }),
            'email': forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':'Email *'
            }),
            'health_id': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Health ID*'
            }),
            'birth': forms.DateInput(attrs={
                'class':'form-control',
                'type':'date'
            }),
            'phone': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Phone *'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class']= 'form-control'
        self.fields['username'].widget.attrs['placeholder']= 'User name *'
        self.fields['password1'].widget.attrs['placeholder']= 'Create a password*'
        self.fields['password2'].widget.attrs['placeholder']= 'Confirm a password*'
        self.fields['password1'].widget.attrs['class']= 'form-control'
        self.fields['password2'].widget.attrs['class']= 'form-control'

    def save(self, commit=True):
        user =super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
