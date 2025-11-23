# apps/strategies/definitions/base_strategy.py
import pandas as pd

from apps.markets.models import TimeFrame

class BaseStrategy:
    """
    Clase base para las estrategias
    """
    def __init__(self, timeframe:TimeFrame, parameters = None):
        self.parameters = parameters or {}
        self.timeframe = timeframe

    def generate_signals(self, data):
        """
        Genera señales de trading a partir de los parámetros y velas
        de entrada. Debe implementarse en la estrategia específica.
        """
    
        raise NotImplementedError("Debe implementarse en la estrategia específica")