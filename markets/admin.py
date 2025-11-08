from django.contrib import admin
from .models import MarketPair, TimeFrame, PairTracking
from django import forms


class PairTrackingForm(forms.ModelForm):
    class Meta:
        model = PairTracking
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Solo readonly si ya existe
            self.fields['pair'].disabled = True
            self.fields['timeframe'].disabled = True

             # Deshabilitar los botones “+ Añadir” y “🔗 Cambiar” del campo ForeignKey
        self.fields['timeframe'].widget.can_add_related = False
        self.fields['timeframe'].widget.can_change_related = False
        self.fields['timeframe'].widget.can_delete_related = False

   
            

class PairTrackingInline(admin.TabularInline):
    model = PairTracking
    form = PairTrackingForm
    extra = 1

   

# Register your models here.
@admin.register(MarketPair)
class MarketPairAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'market_type', 'active')
    actions = None
    list_filter = ('market_type',)
    inlines = [PairTrackingInline] 

    def get_readonly_fields(self, request, obj=None):
        """
       Adicionamos campos readonly despues de crear un objeto
        """
        if obj:  # si el objeto ya existe (estamos editando)
            return self.readonly_fields + ('symbol', 'market_type')
        return self.readonly_fields

    

@admin.register(TimeFrame)
class TimeFrameAdmin(admin.ModelAdmin):
    list_display = ('name', 'minutes', 'active')

    def get_readonly_fields(self, request, obj=None):
        """
       Adicionamos campos readonly despues de crear un objeto
        """
        if obj:  # si el objeto ya existe (estamos editando)
            return self.readonly_fields + ('name', 'minutes')
        return self.readonly_fields


   