# apps/strategies/apps.py
from django.apps import AppConfig


class StrategiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.strategies'

    def ready(self):
        from .definitions.ema_crossover import EmaCrossover
        from .definitions.ema_crossover_rsi import EmaCrossoverRsi
