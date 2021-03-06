from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import Account


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    email = forms.EmailField(label='Email name',max_length=60)
    username = forms.CharField(label='User name',max_length=30)
    first_name =forms.CharField(label='First name',max_length=50)
    last_name = forms.CharField(label='Last name',max_length=50)
    health_id = forms.CharField(label='Health ID',max_length=15)
    birth = forms.DateField(label='Date of birth',)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('username','first_name', 'last_name', 'health_id','email', 'password1', 'password2','birth', 'is_active', 'is_admin', 'is_doctor','is_patient','profile_pic','phone')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    email = forms.EmailField(max_length=60)
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    health_id = forms.CharField(max_length=15)
    birth = forms.DateField()
    password = ReadOnlyPasswordHashField()


    class Meta:
        model = Account
        fields = ('username','first_name', 'last_name', 'health_id','email', 'password', 'birth', 'is_active', 'is_admin', 'is_doctor','is_patient','profile_pic','phone')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username','email', 'birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username','first_name','last_name','email','password')}),
        ('Personal info', {'fields': ('birth','health_id','profile_pic','phone',)}),
        ('Permissions', {'fields': ('is_admin','is_staff','is_doctor','is_patient')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {'fields': ('username','first_name','last_name','email', 'password1', 'password2')}),
        ('Personal info', {'fields': ('birth','health_id',)}),
        ('Permissions', {'fields': ('is_admin','is_staff','is_doctor','is_patient','profile_pic','phone')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(Account, UserAdmin)
# unregister the Group model from admin.
# ... and, since we're not using Django's built-in permissions,
