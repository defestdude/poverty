from datetime import datetime, timedelta
from django.shortcuts import render


from django.conf import settings

from decimal import *

from landing.models import ProphetData




# Create your views here.
def dashboard(request):
    now = datetime.now()
    seven_days_ago = now - timedelta(days=7)

    yesterday = now - timedelta(days=1)
    seconds_in_a_day = 86400
    seconds_so_far = get_total_seconds_so_far()
    duration = (seconds_in_a_day - seconds_so_far) *1000
    pyesterday = 0
    ptoday = 0
    ptoday_lowest = 0
    ptoday_higest = 0
    yhat_data = []
    yhat_min = []
    yhat_max = []
    dates = []
    more_less = "more"
    trend_arrow = "fa-arrow-up"
    trend_arrow_color = "text-danger"
    
    phc_yesterday = ProphetData.objects.all().filter(ds = yesterday)
    phc_today = ProphetData.objects.all().filter(ds = now)
    phc_one_week = ProphetData.objects.all().filter(ds__range=[seven_days_ago, now])
    

    if phc_yesterday.count() > 0:
        pyesterday = phc_yesterday[0].yhat
    
    if phc_today.count() > 0:
        ptoday = phc_today[0].yhat
        ptoday_lowest = phc_today[0].yhat_lower
        ptoday_highest = phc_today[0].yhat_upper

    
    poverty_difference = pyesterday - ptoday

    difference_percentage = (abs(poverty_difference)/pyesterday ) * 100

    rate = abs(poverty_difference) / seconds_in_a_day
    poverty_so_far = 0
    leaving_poverty_today = 0
    entering_poverty_today = 0
    starting_overall_count = 0
    target_overall_count = 0
    start_entry_count = 0
    target_entry_count = 0
    start_leaving_count = 0
    target_leaving_count = 0
    seconds_balance = seconds_in_a_day - seconds_so_far
    escape_rate = 0
    entry_rate = 0

    if poverty_difference < 0:
        print("entering")
        poverty_so_far = pyesterday + (rate * seconds_so_far)
        starting_overall_count = poverty_so_far
        target_overall_count = ptoday
        start_entry_count = 0
        target_entry_count = 0
    else:
        print("leaving")
        more_less = "less"
        trend_arrow = "fa-arrow-down"
        trend_arrow_color = "text-success"
        poverty_so_far = pyesterday - (rate * seconds_so_far)
        entering_poverty_today = poverty_difference - (rate * seconds_so_far)
        starting_overall_count = poverty_so_far
        target_overall_count = ptoday
        start_leaving_count = rate * seconds_so_far
        target_leaving_count = abs(poverty_difference)
        escape_rate = rate

    
    for data in phc_one_week:
        yhat_data.append(int(data.yhat))
        yhat_min.append(int(data.yhat_lower))
        yhat_max.append(int(data.yhat_upper))
        dates.append(data.ds.strftime("%Y-%m-%d"))

    print(yhat_data)
    
    #if poverty_difference < 0:


    context = {
        'page_title' : 'Landing',
        'page_subtitle' : 'Dashboard',
        'page_description' : 'Insights and Analytics',
        'poverty_so_far': poverty_so_far,
        'leaving_poverty_today': abs(leaving_poverty_today),
        'poverty_today': ptoday,
        'rate':rate,
        'duration':duration,
        'starting_overall_count':starting_overall_count,
        'target_overall_count':target_overall_count,
        'start_leaving_count':start_leaving_count,
        'target_leaving_count':target_leaving_count,
        'start_entry_count':start_entry_count,
        'target_entry_count':target_entry_count,
        'poverty_difference':abs(poverty_difference),
        'escape_rate':escape_rate,
        'entry_rate':entry_rate,
        'ptoday_lowest':ptoday_lowest,
        'ptoday_highest':ptoday_highest,
        'yhat':yhat_data,
        'yhat_max':yhat_max,
        'yhat_min':yhat_min,
        'dates':dates,
        'more_less':more_less,
        'difference_percentage':difference_percentage,
        'trend_arrow':trend_arrow,
        'trend_arrow_color':trend_arrow_color

    }
    return render(request, 'landing/dashboard.html', context)

def get_total_seconds_so_far():
    now = datetime.now()
    hours_to_seconds = now.hour * 60 * 60
    minutes_to_seconds = now.minute * 60
    seconds = now.second
    # print(hours_to_seconds)
    return hours_to_seconds + minutes_to_seconds + seconds
    