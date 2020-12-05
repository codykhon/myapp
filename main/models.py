from django import forms
from django.db import models
from UsersAuth.models import Account
from django.core.validators import MinValueValidator
from django.conf import settings

# Create your models here.

class Receipts(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'Doctors')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_patient': True},)
    title = models.CharField('Receipt name', max_length=50)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Receipt'
        verbose_name_plural = 'Receipts'

class Ingredients(models.Model):
    receipt = models.ForeignKey(Receipts, on_delete=models.CASCADE)
    ingredient = models.CharField("Ingredient", max_length=30)
    strength = models.CharField("Strength", max_length=10)
    amount = models.IntegerField("Amount", default=1,validators=[MinValueValidator(1)])
    comments = models.TextField('Comments',  max_length=100)
    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'