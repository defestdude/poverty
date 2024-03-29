from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.shortcuts import render
from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum, Avg

from django.conf import settings

from decimal import *
import os

from landing.models import Inflation, PovertyFeatures, ProphetData, ProphetDataNoCovid
import pandas as pd






# Create your views here.
def dashboard(request):

    temp_path = os.path.join(settings.BASE_DIR, "models")
    filename = os.path.join(temp_path, "forecast.csv")
    empdata = pd.read_csv(filename, index_col=False, delimiter = ',')

    # for i,row in empdata.iterrows():
    #     #here %S means string values 
    #     #xsprint (row['yhat_lower'])
    #     ProphetData.objects.create(ds = datetime.strptime(row['ds'], '%m/%d/%y'), yhat=row['yhat'], yhat_lower=row['yhat_lower'], yhat_upper = row['yhat_upper'])

    now = datetime.now()
    seven_days_ago = now - timedelta(days=7)
    six_months_ago = now + relativedelta(months=-6)

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
    six_months_data = []
    six_months_labels = []
    more_less = "more"
    trend_arrow = "fa-arrow-up"
    trend_arrow_color = "text-danger"
    inflation_data = []
    inflation_labels = []
    male_headcount = 0
    female_headcount = 0
    rate_type_text = "ENTRY RATE"
    leaving_entry = "counters-leaving"
    rate_text = "ESCAPED"
    flash_type = "leave_flashing"
    clock_data_icon = "clock-data-icon"
    data_type_label = "WITH COVID IMPACT"
    ptoday_highest = 0
    
    try:
        if 'switch' in request.GET:
            if request.GET['switch'] == "nocovid":
                phc_yesterday = ProphetDataNoCovid.objects.all().filter(ds = yesterday)
                phc_today = ProphetDataNoCovid.objects.all().filter(ds = now)
                phc_one_week = ProphetDataNoCovid.objects.all().filter(ds__range=[seven_days_ago, now])
                inflation_one_week = Inflation.objects.all().filter(ds__range=[seven_days_ago, now])
                #phc_six_months = ProphetData.objects.all().filter(ds__range=[six_months_ago, now]).group
                phc_six_months = ProphetDataNoCovid.objects.all().filter(ds__range=[six_months_ago, now]).annotate(month=TruncMonth('ds')).values('month').annotate(c=Avg('yhat')).order_by()
                inflation_six_months = Inflation.objects.all().filter(ds__range=[six_months_ago, now]).annotate(month=TruncMonth('ds')).values('month').annotate(c=Avg('yhat')).order_by()
                data_type_label = "WITHOUT COVID IMPACT"
            else:
                phc_yesterday = ProphetData.objects.all().filter(ds = yesterday)
                phc_today = ProphetData.objects.all().filter(ds = now)
                phc_one_week = ProphetData.objects.all().filter(ds__range=[seven_days_ago, now])
                inflation_one_week = Inflation.objects.all().filter(ds__range=[seven_days_ago, now])
                #phc_six_months = ProphetData.objects.all().filter(ds__range=[six_months_ago, now]).group
                phc_six_months = ProphetData.objects.all().filter(ds__range=[six_months_ago, now]).annotate(month=TruncMonth('ds')).values('month').annotate(c=Avg('yhat')).order_by()
                inflation_six_months = Inflation.objects.all().filter(ds__range=[six_months_ago, now]).annotate(month=TruncMonth('ds')).values('month').annotate(c=Avg('yhat')).order_by()
                
        else:
            phc_yesterday = ProphetData.objects.all().filter(ds = yesterday)
            phc_today = ProphetData.objects.all().filter(ds = now)
            phc_one_week = ProphetData.objects.all().filter(ds__range=[seven_days_ago, now])
            inflation_one_week = Inflation.objects.all().filter(ds__range=[seven_days_ago, now])
            #phc_six_months = ProphetData.objects.all().filter(ds__range=[six_months_ago, now]).group
            phc_six_months = ProphetData.objects.all().filter(ds__range=[six_months_ago, now]).annotate(month=TruncMonth('ds')).values('month').annotate(c=Avg('yhat')).order_by()
            inflation_six_months = Inflation.objects.all().filter(ds__range=[six_months_ago, now]).annotate(month=TruncMonth('ds')).values('month').annotate(c=Avg('yhat')).order_by()
        features_today = PovertyFeatures.objects.latest('id')
    except:
        print("no data today")
    

    if phc_yesterday.count() > 0:
        pyesterday = phc_yesterday[0].yhat
    
    if phc_today.count() > 0:
        ptoday = phc_today[0].yhat
        ptoday_lowest = phc_today[0].yhat_lower
        ptoday_highest = phc_today[0].yhat_upper
        male_headcount = ptoday * Decimal(0.5056)
        female_headcount = ptoday - male_headcount

    
    poverty_difference = pyesterday - ptoday

    try:
        difference_percentage = (abs(poverty_difference)/pyesterday ) * 100
    except Exception:
        difference_percentage = 0

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
        clock_data_icon = "clock-data-icon-red"
        rate_text = "ENTERED"
        more_less = "less"
        trend_arrow = "fa-arrow-up"
        trend_arrow_color = "text-danger"
        poverty_so_far = pyesterday + (rate * seconds_so_far)
        starting_overall_count = poverty_so_far
        target_overall_count = ptoday
        start_entry_count = rate * seconds_so_far
        target_entry_count = abs(poverty_difference)
        target_leaving_count = abs(poverty_difference)
        escape_rate = rate
        leaving_entry = "counters-entry"
        flash_type = "enter_flashing"

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
        rate_type_text = "ESCAPE RATE"

    
    for data in phc_one_week:
        yhat_data.append(int(data.yhat))
        yhat_min.append(int(data.yhat_lower))
        yhat_max.append(int(data.yhat_upper))
        dates.append(data.ds.strftime("%Y-%m-%d"))
    
    # for data in inflation_one_week:
    #     inflation_data.append(float(data.yhat))
    #     inflation_labels.append(data.ds.strftime("%Y-%m-%d"))

    for data in phc_six_months:
        six_months_data.append(int(data['c']))
        six_months_labels.append(data['month'].strftime("%b %Y"))
    
    for data in inflation_six_months:
        inflation_data.append(float(data['c']))
        inflation_labels.append(data['month'].strftime("%b %Y"))

    
    
        #print(empdata.head())

   
    
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
        'trend_arrow_color':trend_arrow_color,
        'six_months_data':six_months_data,
        'six_months_labels':six_months_labels,
        'features_today':features_today,
        'inflation_data':inflation_data,
        'inflation_labels':inflation_labels,
        'male_headcount':male_headcount,
        'female_headcount':female_headcount,
        'rate_type_text':rate_type_text,
        'leaving_entering':leaving_entry,
        'rate_text':rate_text,
        'flash_type':flash_type,
        'clock_data_icon':clock_data_icon,
        'data_type':data_type_label

    }
    return render(request, 'landing/dashboard.html', context)

def get_total_seconds_so_far():
    now = datetime.now()
    hours_to_seconds = now.hour * 60 * 60
    minutes_to_seconds = now.minute * 60
    seconds = now.second
    # print(hours_to_seconds)
    return hours_to_seconds + minutes_to_seconds + seconds
    