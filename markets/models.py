from django.db import models

class MarketPair(models.Model):
    MARKET_CHOICES = [
        ('spot', 'Spot'),
        ('future', 'Futures'),
    ]   

    symbol = models.CharField(max_length=20 )
    market_type = models.CharField(max_length=10, choices=MARKET_CHOICES)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.symbol} ({self.market_type})"
    
    class Meta:
        ordering = ['symbol']


class TimeFrame(models.Model):
    name = models.CharField(max_length=10)  # e.g. '1m', '5m', '1h'
    minutes = models.IntegerField()  # conversión a minutos para cálculos
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['minutes']

class PairTracking(models.Model):
    pair = models.ForeignKey(MarketPair, on_delete=models.PROTECT, related_name='trackings')
    timeframe = models.ForeignKey(TimeFrame, on_delete=models.PROTECT, related_name='trackings')
    active = models.BooleanField(default=True)  # Permite activar/desactivar seguimiento sin eliminar

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pair Tracking"
        verbose_name_plural = "Pairs Tracking"
        unique_together = ('pair', 'timeframe')
        ordering = ['pair', 'timeframe']

    def __str__(self):
        return f"{self.pair.symbol} ({self.pair.market_type}) - {self.timeframe.name}"