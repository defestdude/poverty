from django.urls import path
from . import views
from datetime import date

todays_date = date.today()
month = todays_date.month
year = todays_date.year


#URL Conf
urlpatterns  = [
    path('dashboard', views.dashboard, name='dashboard'),
]