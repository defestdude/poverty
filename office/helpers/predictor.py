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

from office.models import PredictionHistory, PredictionTypes, TrainHistory


class Predictor:
    def load_data(self):
        df = pd.read_csv("/Users/donaldmkpanam/Codes/Python/poverty/shocks_with_dates.csv", parse_dates={ 'date': ['year']})
        df = df.set_index('date')
        rng = pd.date_range(df.index.min(), df.index.max() + pd.Timedelta(31, 'D'), freq='D')
        df2 = df.reindex(rng)
        df3 = df2.interpolate('cubicspline')
        df3.tail()
        X = df3.iloc[:,:-1]
        y = df3['pov_hc']
        return X,y

    def calculate_vif_(self,X, thresh=100):
        cols = X.columns
        variables = np.arange(X.shape[1])
        dropped=True
        while dropped:
            dropped=False
            c = X[cols[variables]].values
            vif = [variance_inflation_factor(c, ix) for ix in np.arange(c.shape[1])]

            maxloc = vif.index(max(vif))
            if max(vif) > thresh:
                print('dropping \'' + X[cols[variables]].columns[maxloc] + '\' at index: ' + str(maxloc))
                variables = np.delete(variables, maxloc)
                dropped=True

        #print('Remaining variables:')
        #print(X.columns[variables])
        return X[cols[variables]]

        
    def run_ridge_training(self):
        temp_path = os.path.join(settings.BASE_DIR, "models")
        filename = os.path.join(temp_path, "main_model.sav")

        interpolated = os.path.join(temp_path, "interpolated.csv")
        timenow = datetime.datetime.now()
        X, y = self.load_data()
        newX = self.calculate_vif_(X, thresh=100)
        X_train,X_test,y_train,y_test = train_test_split(newX,y,test_size=0.3,random_state=0)  #newX is the X with reduced features after VIF
        ridgeReg = Ridge(alpha=10)

        ridgeReg.fit(X_train,y_train)
        prediction_type = PredictionTypes.objects.get(id=2)
        ridge_coeffs = ridgeReg.coef_
        #train and test scorefor ridge regression
        train_score_ridge = ridgeReg.score(X_train, y_train)
        test_score_ridge = ridgeReg.score(X_test, y_test)
        TrainHistory.objects.create(train_date=timenow, train_score=test_score_ridge, train_type = prediction_type)
        pickle.dump(ridgeReg, open(filename,'wb'))

        final = newX
        final["pred"] = y.values
        final.reset_index(inplace=True)
        final.to_csv(interpolated)

        print("\nRidge Model............................................\n")
        print("The train score for ridge model is {}".format(train_score_ridge))
        print("The test score for ridge model is {}".format(test_score_ridge))

        self.prophesy()

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
        
        #y_pred = scipy.transform([[shock_date, gce_gdp, gce_es, gedo, sgd, lg_cex, lg_df, liqratio, ltdepo, cbl_ra, cb_msme, vt_nse, kero, brent]])
        y_pred = rf.predict(np.array([gce_gdp, gce_es, gedo, sgd, lg_cex, lg_df, liqratio, ltdepo, pms, cb_msme, vt_nse, kero, brent]).reshape(1, -1))
        output = pd.DataFrame(y_pred)
        #PredictionHistory.objects.create(prediction_date=timenow, prediction_score=output, prediction_type = prediction_type)
        
        print(type(output))
        #output.to_csv('rf.csv')

    def prophesy(self):
        try:
            temp_path = os.path.join(settings.BASE_DIR, "models")
            filename = os.path.join(temp_path, "interpolated.csv")
            filename2 = os.path.join(temp_path, "future.csv")
        except:
            print("Cannot load file")
        df = pd.read_csv(filename)
        df = df.iloc[: , 1:]
        df = df.rename(columns={"index": "ds", "pred": "y"})
        m = Prophet()
        m.fit(df)
        future = m.make_future_dataframe(periods=1730)
        forecast = m.predict(future)
        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(filename2)
        #forecast.to_csv(filename2)
        print("done")