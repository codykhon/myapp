from django.contrib import admin

# Register your models here.

from .models import Receipts, Ingredients

admin.site.register(Receipts)
admin.site.register(Ingredients)