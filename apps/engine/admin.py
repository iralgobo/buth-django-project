# apps/engine/admin.py
from django.contrib import admin
from django import forms
from .models import Backtesting
from apps.strategies.registry import get_strategy_choices, STRATEGY_REGISTRY, DEFAULT_PARAMS
import json
import logging

logger = logging.getLogger(__name__)

class BacktestingForm(forms.ModelForm):
    class Meta:
        model = Backtesting
        fields = '__all__'
    
    class Media:
        js = ("engine/backtesting_dynamic.js",)   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # obtener choices desde el registry

        choices = get_strategy_choices()  # [(k,k), ...]

        # debug rápido (quita o cambia por logger.debug más tarde)
        if not choices:
            # deja trazas útiles si algo falla en la carga de estrategias
            logger.warning("STRATEGY_REGISTRY está vacío: %r", STRATEGY_REGISTRY)

        choices = [("", "---------")] + choices

        # Reemplazamos el campo por un ChoiceField -> admin mostrará <select>
        self.fields['strategie'] = forms.ChoiceField(
            widget=forms.Select(),
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

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        """
        Pasamos DEFAULT_PARAMS al template para usarlo desde JS.
        """
        context['adminform'].form.default_params_json = json.dumps(DEFAULT_PARAMS)
        return super().render_change_form(request, context, add, change, form_url, obj)
    
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        from apps.strategies.registry import DEFAULT_PARAMS
        json_data = json.dumps(DEFAULT_PARAMS)

        form.base_fields['strategie'].widget.attrs.update({
            'data-param-jsons': json_data
        })

        return form