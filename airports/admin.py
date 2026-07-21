from django.contrib import admin
from .models import Country, Airport, Airline, Airplane

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'country')
    list_filter = ('country',)
    search_fields = ('name', 'code', 'country__name')
    list_select_related = ('country',)

@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    search_fields = ('name', 'code')
    filter_horizontal = ('airports',)

@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'capacity', 'airline')
    list_filter = ('airline',)
    search_fields = ('model', 'airline__name')
    list_editable = ('capacity',)
    list_select_related = ('airline',)
