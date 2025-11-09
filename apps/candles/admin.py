from django.contrib import admin
from .models import Candle

# Register your models here.
@admin.register(Candle)
class CandleAdmin(admin.ModelAdmin):
    list_display = ('pair_tracking', 'timestamp', 'open', 'high', 'low', 'close', 'volume')
    actions = None
    list_filter = ('pair_tracking__pair', 'pair_tracking__timeframe')

    # 🔒 Hacer todos los campos readonly
    readonly_fields = [f.name for f in Candle._meta.fields]

    ordering = ['-timestamp']

    # 🔒 Bloquear creación, edición y eliminación
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
     # 🚫 Quitar el historial de cambios del admin
    def history_view(self, request, object_id, extra_context=None):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Historial deshabilitado para este modelo.")

    # 🚫 Quitar botones de guardar / eliminar del detalle
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save'] = False
        extra_context['show_delete'] = False
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)