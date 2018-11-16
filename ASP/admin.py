from django.contrib import admin
from .models import ClinicManager, Supply, Order, OrderDetail, Clinic, Dispatcher, DistanceBetweenClinic
# Register your models here.

admin.site.register(ClinicManager)
admin.site.register(Supply)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Clinic)
admin.site.register(Dispatcher)
admin.site.register(DistanceBetweenClinic)