from datetime import datetime
from django_serverside_datatable.views import ServerSideDatatableView
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from pyparsing import null_debug_action
from office.helpers.data_viewer import PredictionSerializer

from office.models import PredictionHistory, TrainHistory
from .helpers.predictor import Predictor
from landing.models import PovertyFeatures, ProphetData
from .task import run_ridge_training
from rest_framework import viewsets



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
    train_history = {}
    prediction_history = {}
    features_latest = []
    now = datetime.now()

    try:
        train_history = TrainHistory.objects.latest('id')
        prediction_history = PredictionHistory.objects.latest('id')
        features_latest = PovertyFeatures.objects.latest('id')
        print(features_latest)
    except:
        print("No history yet")
    #predictor.run_ridge_training()
    context = {
        'train_history':train_history,
        'prediction_history':prediction_history,
        'features_latest':features_latest,
        'now':now.strftime(("%Y-%m-%d"))
    }
    return render(request, 'office/dashboard.html', context)

def back_office(request):
    context = {}
    predictor = Predictor()

    train_history = {}
    prediction_history = {}

    try:
        train_history = TrainHistory.objects.latest('id')
        prediction_history = PredictionHistory.objects.latest('id')
    except:
        print("no history")
    #run_ridge_training.delay()
    #run_ridge_training()
    #messages.success(request, 'We are running the ridge training, refresh shortly')
    features_head = PovertyFeatures.objects.all()[:5]
    features_tail = PovertyFeatures.objects.all().order_by('-id')[:5]

    context = {
        'train_history':train_history,
        'prediction_history':prediction_history,
        'features_head':features_head,
        'features_tail':features_tail,
        'train_history':train_history,
    }
    return render(request, 'office/office.html', context)


def begin_training(request):
    run_ridge_training.delay()
    messages.success(request, 'We are running the ridge training, refresh shortly')
    return redirect('office')

def shocks_injector(request):
    context = {}
    predictor = Predictor()
    predictor.run_ridge_prediction(request.POST)
    return redirect('office_dashboard')
def user_logout(request):
    logout(request)
    return redirect('login')

class PredictorViewSet(viewsets.ModelViewSet):
    queryset = ProphetData.objects.all().order_by('-ds')
    serializer_class = PredictionSerializer
    
