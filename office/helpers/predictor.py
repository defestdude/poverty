from decimal import Decimal
from django.conf import settings
import pandas as pd
import random
import scipy
from scipy.interpolate import interp1d
import plotly.express as px
from statsmodels.stats.outliers_influence import variance_inflation_factor    
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale 
from sklearn import model_selection
from sklearn.model_selection import RepeatedKFold, train_test_split
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge, RidgeCV, Lasso, LassoCV
from sklearn.metrics import mean_squared_error, r2_score
from scipy.interpolate import interp1d
import os
from pickle5 import pickle
import datetime
from prophet import Prophet
from landing.models import PovertyFeatures

from office.models import PredictionHistory, PredictionTypes, TrainHistory


class Predictor:
    

    def run_ridge_prediction(self, postdata):
        prediction_type = PredictionTypes.objects.get(id=3)
        timenow = datetime.datetime.now()
        temp_path = os.path.join(settings.BASE_DIR, "models")
        filename = os.path.join(temp_path, "main_model.sav")
        rf = pickle.load(open(filename,'rb'))

        shock_date=postdata['shock_date']
        gce_gdp=Decimal(postdata['gce_gdp'])
        gce_es=Decimal(postdata['gce_es'])
        gedo=Decimal(postdata['gedo'])
        sgd=Decimal(postdata['sgd'])
        lg_cex=Decimal(postdata['lg_cex'])
        lg_df=Decimal(postdata['lg_df'])
        liqratio=Decimal(postdata['liqratio'])
        ltdepo=Decimal(postdata['ltdepo'])
        pms=Decimal(postdata['pms'])
        cb_msme=Decimal(postdata['cb_msme'])
        vt_nse=Decimal(postdata['vt_nse'])
        kero=Decimal(postdata['kero'])
        brent=Decimal(postdata['brent'])

        # shock_date=postdata['shock_date']
        # gce_gdp=postdata['gce_gdp'],
        # gce_es=postdata['gce_es'],
        # gedo=postdata['gedo'],
        # sgd=postdata['sgd'],
        # lg_cex=postdata['lg_cex'],
        # lg_df=postdata['lg_df'],
        # liqratio=postdata['liqratio'],
        # ltdepo=postdata['ltdepo'],
        # pms=postdata['pms'],
        # cb_msme=postdata['cb_msme'],
        # vt_nse=postdata['vt_nse'],
        # kero=postdata['kero'],
        # brent=postdata['brent']
        
        #y_pred = scipy.transform([[shock_date, gce_gdp, gce_es, gedo, sgd, lg_cex, lg_df, liqratio, ltdepo, cbl_ra, cb_msme, vt_nse, kero, brent]])
        y_pred = rf.predict(np.array([gce_gdp, gce_es, gedo, sgd, lg_cex, lg_df, liqratio, ltdepo, pms, cb_msme, vt_nse, kero, brent]).reshape(1, -1))
        output = pd.DataFrame(y_pred)
        PredictionHistory.objects.create(prediction_date=timenow, prediction_score=output.iat[0,0], prediction_type = prediction_type)
        PovertyFeatures.objects.create(
            feature_date=postdata['shock_date'],
            gce_gdp=postdata['gce_gdp'],
            gce_es=postdata['gce_es'],
            gedo=postdata['gedo'],
            sgd=postdata['sgd'],
            lg_cex=postdata['lg_cex'],
            lg_df=postdata['lg_df'],
            liqratio=postdata['liqratio'],
            ltdepo=postdata['ltdepo'],
            pms=postdata['pms'],
            cb_msme=postdata['cb_msme'],
            vt_nse=postdata['vt_nse'],
            kero=postdata['kero'],
            brent=postdata['brent']
        )
        
        print(output.iat[0,0])
        #output.to_csv('rf.csv')

    