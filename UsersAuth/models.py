from django.contrib.auth import default_app_config
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, health_id, username, birth,password):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")
        user = self.model(
            email = self.normalize_email(email),
            username= username,
            first_name= first_name,
            last_name = last_name,
            birth = birth,
            health_id= health_id,
            password = password
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, health_id, username, birth, password ):
        user = self.create_user(
            email = self.normalize_email(email),
            username= username,
            first_name= first_name,
            last_name = last_name,
            birth = birth,
            health_id= health_id,
            password = password
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user



class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=60, unique =True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    health_id = models.CharField(max_length=15)
    birth = models.DateField()
    profile_pic = models.ImageField(default='default.png',blank=True)
    phone = models.CharField(max_length=25, blank=True)
    is_doctor = models.BooleanField(default=False, blank=True)
    is_patient = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'health_id', 'birth',]

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm , obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True