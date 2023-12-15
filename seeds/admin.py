from django.contrib import admin
from .models import Seeds, GrowingInfo

@admin.register(Seeds)
class SeedsAdmin(admin.ModelAdmin):
    list_display = ('species_name', 'cbd', 'thc', 'description')
    search_fields = ('species_name', 'description')  # Puedes personalizar esto según tus necesidades

@admin.register(GrowingInfo)
class GrowingInfoAdmin(admin.ModelAdmin):
    list_display = ('seed_id', 'flowering_time', 'harvest_time', 'grow_dificulty', 'yield_outdoor', 'yield_indoor')

