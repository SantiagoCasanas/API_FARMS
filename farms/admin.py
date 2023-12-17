from django.contrib import admin
from .models import Farm, Parcel

class FarmAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'farm_name', 'longitude', 'latitude', 'date_creation_farm')
    search_fields = ('farm_name', 'user_id')

class ParcelAdmin(admin.ModelAdmin):
    list_display = ('farm', 'seed', 'width', 'length', 'crop_modality', 'date_creation_parcel')
    list_filter = ('crop_modality',)
    search_fields = ('farm__farm_name', 'seed__seed_name')

admin.site.register(Farm, FarmAdmin)
admin.site.register(Parcel, ParcelAdmin)