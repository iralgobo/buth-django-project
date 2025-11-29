# apps/strategies/definitions/ema_crossoever.py
from .base_strategy import BaseStrategy
from apps.strategies.registry import register_strategy

@register_strategy("ema_crossover", default_params={"fast": 12, "slow": 26})
class EmaCrossover(BaseStrategy):
    def generate_signals(self, data):
        pass