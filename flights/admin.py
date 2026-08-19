from django.contrib import admin
from .models import Flight, Ticket, Order


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):

    list_display = ('id', 'flight_number', 'departure_airport', 'arrival_airport', 'airplane', 'departure_time', 'status')
    list_select_related = ('airplane', 'departure_airport', 'arrival_airport')
    list_filter = ('status', 'departure_time', 'airplane')
    search_fields = ('flight_number',)
    list_editable = ('status',)
    ordering = ('-departure_time',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'flight', 'order', 'seat_number', 'price', 'status')
    list_select_related = ('flight', 'order')
    list_filter = ('status',)
    search_fields = ('seat_number', 'flight__flight_number')
    list_editable = ('status',)