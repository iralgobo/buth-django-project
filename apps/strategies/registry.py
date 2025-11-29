# apps/strategies/registry.py

STRATEGY_REGISTRY = {}
DEFAULT_PARAMS = {}

def register_strategy(name, default_params=None):
    """
    Decorador para registrar clases de estrategia.
    """
    def wrapper(cls):
        STRATEGY_REGISTRY[name] = cls
        DEFAULT_PARAMS[name] = default_params or {}
        cls.strategy_name = name  # opcional, útil para debug
        return cls
    return wrapper

def get_strategy_choices():
    return [(key, key) for key in STRATEGY_REGISTRY.keys()]