from django.contrib.auth.models import Group
from django.http.response import Http404
from .models import Account
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from main.models import Receipts, Ingredients
from .healthids import DOCTORS_ID

# Create your views here.

def loginview(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password= password)
        if form.is_valid():
            login(request, user)
            return redirect('main:home')
    else:
        form = AuthenticationForm()
    return render (request, 'UsersAuth/login.html', {'form':form})

def register(request):
    error = ""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user= Account.objects.get(username = request.POST['username'])
            health_id = request.POST['health_id']
            if health_id in DOCTORS_ID:
                user.is_doctor = True
                user.is_patient = False
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('UsersAuth:login')
            else:
                user.is_patient = True
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('UsersAuth:login')
        else:
            error = 'Form is not valid'
    form = RegisterForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'UsersAuth/register.html', context)

def logoutview(request):
    if request.method == 'POST':
        logout(request)
        return redirect('main:home')

def profile_view(request, user_id):
    try:
        user = Account.objects.get( id = user_id)
        obj = Receipts.objects.filter(patient = user)
    except:
        raise Http404("Not found")
    context = {
        'user':user,
        'receipts':obj,
    }
    return render(request, 'UsersAuth/profile.html', context)