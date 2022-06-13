from django.db import models
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

# Create your models here.
class PovertyFeatures(models.Model):
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