from django.db import models
from apps.markets.models import MarketPair, TimeFrame

# Create your models here.

class Candle(models.Model):
    # Clave primaria grande para no preocuparse por el id
    id = models.BigAutoField(primary_key=True)

    # Foreign key al seguimiento de pares
    pair_tracking = models.ForeignKey(
        'markets.PairTracking',
        on_delete=models.PROTECT,
        related_name='candles'
    )

    # Timestamp de la vela
    timestamp = models.DateTimeField()
    timestamp_unix = models.BigIntegerField(default=0)

    # Valores OHLC
    open = models.DecimalField(max_digits=20, decimal_places=8)
    high = models.DecimalField(max_digits=20, decimal_places=8)
    low = models.DecimalField(max_digits=20, decimal_places=8)
    close = models.DecimalField(max_digits=20, decimal_places=8)
    volume = models.DecimalField(max_digits=30, decimal_places=8)

    class Meta:
        ordering = ['timestamp']
        indexes = [
            # Índice compuesto para búsquedas rápidas por par y rango de tiempo
            models.Index(fields=['pair_tracking', 'timestamp']),
            # Índices individuales opcionales si consultas por timestamp solo
            models.Index(fields=['timestamp']),
        ]
        # Unique constraint para evitar duplicados
        constraints = [
            models.UniqueConstraint(
                fields=['pair_tracking', 'timestamp'],
                name='unique_candle_per_pair_time'
            )
        ]

    def __str__(self):
        return f"{self.pair_tracking} {self.timestamp}"