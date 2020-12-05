from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .models import Receipts, Ingredients
from .forms import ReceiptForm, IngredientForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from UsersAuth.models import Account
# Create your views here.
@login_required(login_url = 'UsersAuth:login')
def index(request):
    users = Account.objects.order_by('id')
    receipts = Receipts.objects.filter(patient = request.user)
    return render(request, 'main/index.html', {'receipts':receipts, 'users':users})

def detail(request, receipt_id):
    try:
        a = Receipts.objects.get( id = receipt_id)
    except:
        raise Http404("Not found")
    ingredients = a.ingredients_set.all()
    return render(request, 'main/detail.html',{'receipt':a, 'ingredients': ingredients})

def add_ingredient(request, receipt_id):
    try:
       a = Receipts.objects.get( id = receipt_id)
    except:
       raise Http404("Not found")
    a.ingredients_set.create(ingredient =  request.POST['ingredient'], strength = request.POST['strength'], amount = request.POST['amount'], comments = request.POST['comments'])

    return HttpResponseRedirect( reverse('main:detail', args=(a.id,)) )

def about(request):
    return render(request, 'main/about.html')

def create(request):
    error = ""
    if request.method == 'POST':
        form = ReceiptForm(request.POST)
        if  form.is_valid():
            obj = form.save(commit = False)
            obj.author = request.user
            rcid = obj.patient.id
            form.save()
            return HttpResponseRedirect( reverse('UsersAuth:profile', args=(rcid,)) )
        else:
            error = 'Form is not valid'

    form =  ReceiptForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'main/create.html', context)

def delete_rec(request, receipt_id):
    receipt = get_object_or_404(Receipts, id=receipt_id)
    user = receipt.patient.id
    if request.method == 'POST':
        receipt.delete()
    return HttpResponseRedirect( reverse('UsersAuth:profile', args=(user,)) )

def ing_delete(request, receipt_id, el_id):
    try:
        a = Receipts.objects.get( id = receipt_id)
        ingredient = get_object_or_404(Receipts, id=el_id)
    except:
        raise Http404("Not found")
    if request.method == 'POST':
        ingredient.delete()
    return HttpResponseRedirect( reverse('main:detail', args=(a.id,)) )