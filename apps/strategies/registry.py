# apps/strategies/registry.py

STRATEGY_REGISTRY = {}

def register_strategy(name):
    """
    Decorador para registrar clases de estrategia.
    """
    def wrapper(cls):
        STRATEGY_REGISTRY[name] = cls
        cls.strategy_name = name  # opcional, útil para debug
        return cls
    return wrapper

def get_strategy_choices():
    return [(key, key) for key in STRATEGY_REGISTRY.keys()]