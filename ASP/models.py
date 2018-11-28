import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

# Create your models here.
class Location(models.Model):
	name = models.CharField(max_length=200)
	latitude = models.DecimalField(max_digits=10, decimal_places=6)
	longitude = models.DecimalField(max_digits=10, decimal_places=6)
	altitude = models.IntegerField()
	def __str__(self):
		return f'{self.pk} {self.name}'
	def __lt__(self, other):
		return True

class DistanceBetweenLocation(models.Model):
	location1 = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location1')
	location2 = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location2')
	distance = models.DecimalField(max_digits=6, decimal_places=2)
	def __str__(self):
		return f'{self.pk} {self.distance}'

class Invitation(models.Model):
	email = models.CharField(max_length=200)
	role = models.CharField(max_length=20)
	def __str__(self):
		return f'{self.pk} {self.email} {self.role}'

class ClinicManager(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	clinic = models.OneToOneField(Location, on_delete=models.CASCADE)
	def __str__(self):
		return f'{self.pk} {self.user.first_name} {self.user.last_name}'

class Dispatcher(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	def __str__(self):
		return f'{self.pk} {self.user.first_name} {self.user.last_name}'

class WarehousePersonnel(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	def __str__(self):
		return f'{self.pk} {self.user.first_name} {self.user.last_name}'

class Supply(models.Model):
	name = models.CharField(max_length=200)
	category = models.CharField(max_length=200)
	weight = models.DecimalField(max_digits=4, decimal_places=2)
	image = models.ImageField(default = "default.png", blank=True)
	def __str__(self):
		return f'{self.pk} {self.name}'

class Order(models.Model):
	owner = models.ForeignKey(ClinicManager, on_delete=models.CASCADE)
	priority = models.CharField(max_length=200, blank=True)
	weight = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
	location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE)
	status = models.CharField(max_length=200)
	placeTime = models.DateTimeField(default=datetime.now())
	dispatchTime = models.DateTimeField(default=datetime.now())
	deliveredTime = models.DateTimeField(default=datetime.now())
	def __str__(self):
		return f'{self.pk}'
	def __lt__(self, other):
		if (self.priority == other.priority):
			return self.placeTime < other.placeTime
		elif (self.priority == "High"):
			return True
		elif (other.priority == "Low"):
			return True
		else:
			return False

class OrderDetail(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	supply = models.ForeignKey(Supply, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	def __str__(self):
		return f'{self.order.pk}: {self.supply.name} {self.quantity}'