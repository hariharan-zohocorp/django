from sample.models import Berth_Cost, Passengers, Routes, Ticket, Train, Train_Seats
from django.contrib import admin

# Register your models here.
admin.site.register(Train)
admin.site.register(Train_Seats)
admin.site.register(Ticket)
admin.site.register(Routes)
admin.site.register(Passengers)
admin.site.register(Berth_Cost)
