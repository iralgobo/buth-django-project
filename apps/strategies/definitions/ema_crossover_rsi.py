# apps/strategies/definitions/ema_crossover_rsi.py
from apps.strategies.definitions.base_strategy import BaseStrategy
from apps.strategies.registry import register_strategy

@register_strategy("ema_crossover_rsi", default_params={"fast": 12, "slow": 26, "rsi": 14})
class EmaCrossoverRsi(BaseStrategy):
    def generate_signals(self, data):
        pass