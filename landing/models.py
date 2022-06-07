from django.db import models

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