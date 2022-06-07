from django.shortcuts import render


from django.conf import settings

from decimal import *




# Create your views here.
def dashboard(request):
    
    context = {
        'page_title' : 'Landing',
        'page_subtitle' : 'Dashboard',
        'page_description' : 'Insights and Analytics',

    }
    return render(request, 'landing/dashboard.html', context)