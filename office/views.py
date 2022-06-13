from django_serverside_datatable.views import ServerSideDatatableView
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages

from office.models import PredictionHistory, TrainHistory
from .helpers.predictor import Predictor
from landing.models import PovertyFeatures
from .task import run_ridge_training



def route_landing(request):
    context = {}
    return render(request,'office/login.html', context)


def user_login(request):
    context = {}
    if request.method == 'POST':
        #print("none")
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            messages.error(request, 'User does not exist')
            print("user does not exist")
            return render(request,'office/login.html', context)

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            print("error1")
            return redirect('office_dashboard')
        else:
            print("error2")
            messages.error(request, "Username or password does not exist ")
            return render(request,'office/login.html', context)          
    else:
        print("error3")
        return render(request,'office/login.html', context)

def dashboard(request):
    context = {}
    predictor = Predictor()
    train_history = TrainHistory.objects.latest('id')
    prediction_history = PredictionHistory.objects.latest('id')
    #predictor.run_ridge_training()
    context = {
        'train_history':train_history,
        'prediction_history':prediction_history
    }
    return render(request, 'office/dashboard.html', context)

def back_office(request):
    context = {}
    predictor = Predictor()
    train_history = TrainHistory.objects.latest('id')
    prediction_history = PredictionHistory.objects.latest('id')
    run_ridge_training.delay()
    #run_ridge_training()
    messages.success(request, 'We are running the ridge training, refresh shortly')
    context = {
        'train_history':train_history,
        'prediction_history':prediction_history
    }
    return render(request, 'office/office.html', context)

def shocks_injector(request):
    context = {}
    predictor = Predictor()
    predictor.run_ridge_prediction(request.POST)
    return redirect('office_dashboard')
def user_logout(request):
    logout(request)
    return redirect('login')

class ItemListView(ServerSideDatatableView):
	queryset = PovertyFeatures.objects.all()
	columns = ['name', 'code', 'description']