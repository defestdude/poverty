from django.db import models
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

# Create your models here.
class poverty_features(models.Model):
    gre_tc = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    gre_rc = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    gre_ga = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    gce_gdp = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    gedo = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    sdg = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    lg_rex = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    lg_cex = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    lg_df = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    liqratio = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    ltdepo = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    cbl_ra = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    cb_msme = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    vt_nse = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    

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