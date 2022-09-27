import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.conf import settings
import os
from pickle5 import pickle
import datetime
#from prophet import Prophet
from sklearn.model_selection import RepeatedKFold, train_test_split
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge, RidgeCV, Lasso, LassoCV
from sklearn.metrics import mean_squared_error, r2_score
from scipy.interpolate import interp1d
from landing.models import Inflation, PovertyFeatures
from office.models import PredictionHistory, PredictionTypes, TrainHistory
import pandas as pd
#import numpy as np
from scipy.interpolate import interp1d
import plotly.express as px
from statsmodels.stats.outliers_influence import variance_inflation_factor

from celery import shared_task

@shared_task
def run_ridge_training():
    temp_path = os.path.join(settings.BASE_DIR, "models")
    filename = os.path.join(temp_path, "main_model.sav")

    interpolated = os.path.join(temp_path, "interpolated.csv")
    timenow = datetime.datetime.now()
    X, y = load_data()
    newX = calculate_vif_(X, thresh=100)
    X_train,X_test,y_train,y_test = train_test_split(newX,y,test_size=0.3,random_state=0)  #newX is the X with reduced features after VIF
    #X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=0)
    ridgeReg = Ridge(alpha=10)

    ridgeReg.fit(X_train,y_train)
    prediction_type = PredictionTypes.objects.get(id=2)
    ridge_coeffs = ridgeReg.coef_
    #train and test scorefor ridge regression
    train_score_ridge = ridgeReg.score(X_train, y_train)
    test_score_ridge = ridgeReg.score(X_test, y_test)
    TrainHistory.objects.create(train_date=timenow, train_score=test_score_ridge, train_type = prediction_type)
    pickle.dump(ridgeReg, open(filename,'wb'))

    final = X
    final["pred"] = y.values
    final.reset_index(inplace=True)
    final.to_csv(interpolated)

    # gce_gdp = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    # gce_es = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    # gedo = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    # sgd = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    # lg_cex = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    # lg_df = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    # liqratio = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    # ltdepo = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    # pms = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    # cb_msme = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    # vt_nse = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    # kero = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    # brent = models.DecimalField(max_digits=21, decimal_places=10, null=False)

    PovertyFeatures.truncate()
    #print(final)
    for index, row in final.iterrows():
        PovertyFeatures.objects.create(
            feature_date = row['index'],
            gce_gdp=row['gce_gdp'],
            gce_es=row['gce_es'],
            gedo=row['gedo'],
            sgd=row['sgd'],
            lg_cex=row['lg_cex'],
            lg_df=row['lg_df'],
            liqratio=row['liqratio'],
            ltdepo=row['ltdepo'],
            pms=row['pms'],
            cb_msme=row['cb_msme'],
            vt_nse=row['vt_nse'],
            kero=row['kero'],
            brent=row['brent']
        )
       

    print("\nRidge Model............................................\n")
    print("The train score for ridge model is {}".format(train_score_ridge))
    print("The test score for ridge model is {}".format(test_score_ridge))

    prophesy()
@shared_task
def load_data():
    temp_path = os.path.join(settings.BASE_DIR, "models")
    filename = os.path.join(temp_path, "shocks_with_dates.csv")
    df = pd.read_csv(filename, parse_dates={ 'date': ['year']})
    df = df.set_index('date')
    rng = pd.date_range(df.index.min(), df.index.max() + pd.Timedelta(31, 'D'), freq='D')
    df2 = df.reindex(rng)
    df3 = df2.interpolate('cubicspline')
    df3.tail()
    X = df3.iloc[:,:-1]
    y = df3['pov_hc']
    return X,y

@shared_task
def calculate_vif_(X, thresh=100):
    cols = X.columns
    # variables = np.arange(X.shape[1])
    # dropped=True
    # while dropped:
    #     dropped=False
    #     c = X[cols[variables]].values
    #     vif = [variance_inflation_factor(c, ix) for ix in np.arange(c.shape[1])]

    #     maxloc = vif.index(max(vif))
    #     if max(vif) > thresh:
    #         print('dropping \'' + X[cols[variables]].columns[maxloc] + '\' at index: ' + str(maxloc))
    #         variables = np.delete(variables, maxloc)
    #         dropped=True

    #print('Remaining variables:')
    #print(X.columns[variables])
    #return X[cols[variables]]
@shared_task
def prophesy():
    try:
        temp_path = os.path.join(settings.BASE_DIR, "models")
        filename = os.path.join(temp_path, "interpolated.csv")
        filename2 = os.path.join(temp_path, "future.csv")
    except:
        print("Cannot load file")
    df = pd.read_csv(filename)
    df = df.iloc[: , 1:]
    df = df.rename(columns={"index": "ds", "pred": "y"})
    # m = Prophet()
    # m.fit(df)
    # future = m.make_future_dataframe(periods=1730)
    # forecast = m.predict(future)
    # forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(filename2)

    # ProphetData.truncate()
    # for index, row in forecast.iterrows():
    #     ProphetData.objects.create(
    #         ds = row['ds'],
    #         yhat=row['yhat'],
    #         yhat_lower=row['yhat_lower'],
    #         yhat_upper=row['yhat_upper'],
    #     )
    #forecast.to_csv(filename2)
    print("done")

@shared_task
def upload_inflation():    
    temp_path = os.path.join(settings.BASE_DIR, "models")
    filename = os.path.join(temp_path, "forecast_inflation.csv")
    #df = pd.read_csv(filename, parse_dates={ 'date': ['ds']})
    df = pd.read_csv(filename)
    Inflation.truncate()
    #print(df)
    for index, row in df.iterrows():
        #datestr = row['ds'].strftime("%d/%m/%Y")
        testdate = datetime.datetime.strptime(row['ds'], "%d/%m/%Y")
        testdate2 = testdate.strftime('%Y-%m-%d')
        # print(testdate)
        # print(testdate2)
        Inflation.objects.create(
            ds = testdate,
            yhat=row['yhat_main'],
            yhat_lower=row['yhat_lower_main'],
            yhat_upper=row['yhat_upper_main'],
        )
        #print(row['date'], row['yhat_main'])
