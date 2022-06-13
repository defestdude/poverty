from datetime import datetime, timedelta
from django.shortcuts import render


from django.conf import settings

from decimal import *

from landing.models import ProphetData




# Create your views here.
def dashboard(request):
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    seconds_in_a_day = 86400
    seconds_so_far = get_total_seconds_so_far()
    duration = (seconds_in_a_day - seconds_so_far)
    
    phc_yesterday = ProphetData.objects.all().filter(ds = yesterday)[0]
    phc_today = ProphetData.objects.all().filter(ds = now)[0]

    poverty_difference = (phc_today.yhat - phc_yesterday.yhat)*100

    rate = abs(poverty_difference) / seconds_in_a_day
    poverty_so_far = 0
    leaving_poverty_today = 0
    entering_poverty_today = 0

    if poverty_difference < 0:
        poverty_so_far = phc_today.yhat - (rate * seconds_so_far)
        leaving_poverty_today = poverty_difference + (rate * seconds_so_far)

    else:
        poverty_so_far = phc_today.yhat + (rate * seconds_so_far)

    print(abs(poverty_difference))
    print(leaving_poverty_today)
    #if poverty_difference < 0:


    context = {
        'page_title' : 'Landing',
        'page_subtitle' : 'Dashboard',
        'page_description' : 'Insights and Analytics',
        'poverty_so_far': poverty_so_far,
        'leaving_poverty_today': leaving_poverty_today,
        'poverty_today': phc_today.yhat,
        'rate':rate,
        'duration':duration,
        'poverty_difference':abs(poverty_difference)

    }
    return render(request, 'landing/dashboard.html', context)

def get_total_seconds_so_far():
    now = datetime.now()
    hours_to_seconds = now.hour * 60 * 60
    minutes_to_seconds = now.minute * 60
    seconds = now.second
    return hours_to_seconds + minutes_to_seconds + seconds
    