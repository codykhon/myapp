from main.views import add_ingredient
from django.urls import path, include
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('create/', views.create, name = 'create'),
    path('<int:receipt_id>/receipt', views.detail, name = 'detail'),
    path('<int:receipt_id>/receipt/add_ingredient', views.add_ingredient, name ='add_ingredient'),
    path('<int:receipt_id>/receipt/delete',views.delete_rec, name='delete'),
    path('<int:receipt_id>/receipt/ing_delete', views.ing_delete, name='ing_delete'),
    ]
