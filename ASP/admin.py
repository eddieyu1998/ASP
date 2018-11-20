from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(ClinicManager)
admin.site.register(Supply)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Clinic)
admin.site.register(Dispatcher)
admin.site.register(DistanceBetweenClinic)
admin.site.register(Location)
admin.site.register(WarehousePersonnel)
admin.site.register(Invitation)
admin.site.register(User_test)