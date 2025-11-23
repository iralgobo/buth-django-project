# app/engine/models.py
from django.db import models

# Create your models here.
class Backtesting(models.Model):
    tracking = models.ForeignKey('markets.PairTracking', on_delete=models.CASCADE)
    strategie = models.CharField(max_length=50)
    initial_balance = models.DecimalField(
        max_digits=20, decimal_places=8, default=1000.0
    )
    days_back = models.IntegerField(default=100)
    parameters = models.JSONField()
    

    def __str__(self):
        return f"{self.tracking} - {self.strategie}"
    
   
    