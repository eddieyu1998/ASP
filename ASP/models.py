import datetime
from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.
class ClinicManager(models.Model):
	firstName = models.CharField(max_length=200)
	lastName = models.CharField(max_length=200)
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	def __str__(self):
		return f'{self.firstName} {self.lastName}'

class Supply(models.Model):
	name = models.CharField(max_length=200)
	category = models.CharField(max_length=200)
	weight = models.DecimalField(max_digits=4, decimal_places=2)
	image = models.ImageField(default = "default.png", blank=True)
	def __str__(self):
		return f'{self.name}'

class Order(models.Model):
	owner = models.ForeignKey(ClinicManager, on_delete=models.CASCADE)
	priority = models.CharField(max_length=200, blank=True)
	weight = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
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


class OrderDetail(models.Model): #change to orderitem
	orderID = models.ForeignKey(Order, on_delete=models.CASCADE)
	supplyID = models.ForeignKey(Supply, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	def __str__(self):
		return f'{self.orderID.pk}: {self.supplyID.name} {self.quantity}'

class Clinic(models.Model):
	manager = models.OneToOneField(ClinicManager, null=True, blank=True, on_delete=models.SET_NULL)
	name = models.CharField(max_length=200)
	latitude = models.DecimalField(max_digits=10, decimal_places=6)
	longitude = models.DecimalField(max_digits=10, decimal_places=6)
	altitude = models.IntegerField()
	def __str__(self):
		return f'{self.pk} {self.name}'
	def __lt__(self, other):
		return True

class Location(models.Model):
	name = models.CharField(max_length=200)
	latitude = models.DecimalField(max_digits=10, decimal_places=6)
	longitude = models.DecimalField(max_digits=10, decimal_places=6)
	altitude = models.IntegerField()
	def __str__(self):
		return f'{self.pk} {self.name}'

class Dispatcher(models.Model):
	firstName = models.CharField(max_length=200)
	lastName = models.CharField(max_length=200)
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	def __str__(self):
		return f'{self.firstName} {self.lastName}'

class DistanceBetweenClinic(models.Model):
	clinic1 = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='clinic1')
	clinic2 = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='clinic2')
	distance = models.DecimalField(max_digits=6, decimal_places=2)
	def __str__(self):
		return f'{self.pk} {self.distance}'

class WarehousePersonnel(models.Model):
	firstName = models.CharField(max_length=200)
	lastName = models.CharField(max_length=200)
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	def __str__(self):
		return f'{self.firstName} {self.lastName}'

class Invitation(models.Model):
	email = models.CharField(max_length=200)
	role = models.CharField(max_length=20)
	def __str__(self):
		return f'{self.pk} {self.email} {self.role}'