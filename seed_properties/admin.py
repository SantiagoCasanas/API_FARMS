from django.contrib import admin
from .models import Flavor, Smell, Effect, SeedFlavor, SeedSmell, SeedEffect

@admin.register(Flavor)
class FlavorAdmin(admin.ModelAdmin):
    list_display = ('flavor_name',)

@admin.register(Smell)
class SmellAdmin(admin.ModelAdmin):
    list_display = ('smell_name',)

@admin.register(Effect)
class EffectAdmin(admin.ModelAdmin):
    list_display = ('effect_name',)

@admin.register(SeedFlavor)
class SeedFlavorAdmin(admin.ModelAdmin):
    list_display = ('seed_id', 'flavor_id')

@admin.register(SeedSmell)
class SeedSmellAdmin(admin.ModelAdmin):
    list_display = ('seed_id', 'smell_id')

@admin.register(SeedEffect)
class SeedEffectAdmin(admin.ModelAdmin):
    list_display = ('seed_id', 'effect_id')
