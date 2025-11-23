# apps/engine/admin.py
from django.contrib import admin
from django import forms
from .models import Backtesting
from apps.strategies.registry import get_strategy_choices, STRATEGY_REGISTRY
import logging

logger = logging.getLogger(__name__)

class BacktestingForm(forms.ModelForm):
    class Meta:
        model = Backtesting
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # obtener choices desde el registry
        choices = get_strategy_choices()  # [(k,k), ...]

        # debug rápido (quita o cambia por logger.debug más tarde)
        if not choices:
            # deja trazas útiles si algo falla en la carga de estrategias
            logger.warning("STRATEGY_REGISTRY está vacío: %r", STRATEGY_REGISTRY)

        # Reemplazamos el campo por un ChoiceField -> admin mostrará <select>
        self.fields['strategie'] = forms.ChoiceField(
            choices=choices,
            required=True,
            label=self.fields['strategie'].label if 'strategie' in self.fields else "Strategie"
        )

# Register your models here.
@admin.register(Backtesting)
class BacktestingAdmin(admin.ModelAdmin):
    form = BacktestingForm

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "strategie":
            kwargs['choices'] = get_strategy_choices()
        return super().formfield_for_choice_field(db_field, request, **kwargs)