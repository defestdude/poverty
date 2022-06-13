from django.db import models

# Create your models here.

class PredictionTypes(models.Model):
    prediction_type = models.CharField(max_length=20, null=True)
class PredictionHistory(models.Model):
    prediction_date = models.DateTimeField()
    prediction_score = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    prediction_type = models.ForeignKey(PredictionTypes, on_delete=models.SET_NULL, null=True)

class TrainHistory(models.Model):
    train_date = models.DateTimeField()
    train_score = models.DecimalField(max_digits=21, decimal_places=10, null=False)
    train_type = models.ForeignKey(PredictionTypes, on_delete=models.SET_NULL, null=True)
    