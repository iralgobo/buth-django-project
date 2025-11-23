# apps/strategies/definitions/ema_crossover_rsi.py
from apps.strategies.definitions.base_strategy import BaseStrategy
from apps.strategies.registry import register_strategy

@register_strategy("ema_crossover_rsi")
class EmaCrossoverRsi(BaseStrategy):
    def generate_signals(self, data):
        pass