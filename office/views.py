from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages


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
            print("test1")
            return redirect('office_dashboard')
        else:
            print("test2")
            messages.error(request, "Username or password does not exist ")
            return render(request,'office/login.html', context)
            
    else:
        print("test3")
        return render(request,'office/login.html', context)

def dashboard(request):
    context = {}
    return render(request, 'office/dashboard.html', context)

def user_logout(request):
    logout(request)
    return redirect('login')