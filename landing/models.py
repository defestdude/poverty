from django.db import connection, models
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

# Create your models here.
class PovertyFeatures(models.Model):
    feature_date = models.DateField(null=True)
    gce_gdp = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    gce_es = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    gedo = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    sgd = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    lg_cex = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    lg_df = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    liqratio = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    ltdepo = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    pms = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    cb_msme = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    vt_nse = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    kero = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    brent = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    @classmethod
    def truncate(self):
        cursor = connection.cursor()
        cursor.execute('TRUNCATE TABLE landing_povertyfeatures')
    
    #forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
class ProphetData(models.Model):
    ds = models.DateField(null=True)
    yhat = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    yhat_lower = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    yhat_upper = models.DecimalField(max_digits=21, decimal_places=10, null=False)

    class Meta:
        ordering = ['id']

    @classmethod
    def truncate(self):
        cursor = connection.cursor()
        cursor.execute('TRUNCATE TABLE landing_prophetdata')

class Inflation(models.Model):
    ds = models.DateField(null=True)
    yhat = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    yhat_lower = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    yhat_upper = models.DecimalField(max_digits=21, decimal_places=10, null=False)

    class Meta:
        ordering = ['id']

    @classmethod
    def truncate(self):
        cursor = connection.cursor()
        cursor.execute('TRUNCATE TABLE landing_inflation')
    
class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None