from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from heapq import heappush, heappop
from decimal import *
import csv

from ASP.models import ClinicManager, Supply, Order, OrderDetail, Clinic, Dispatcher, DistanceBetweenClinic

# Create your views here.
def DefaultView(request):
	return HttpResponse("The view is working.")

class browse(View):
	model = Supply
	template_name = 'ASP/supply_list.html'

	def get(self, request, *args, **kwargs):
		objects = self.model.objects.all()
		return render(request, self.template_name, {'object_list' : objects})

	def post(self, request, *args, **kwargs):
		category = request.POST.get('category', False)
		search = request.POST.get('search', False)
		if search:
			objects = self.model.objects.filter(name__contains=search)
		elif (category == "all"):
			objects = self.model.objects.all()
		else:
			objects = self.model.objects.filter(category=category)
		return render(request, self.template_name, {'object_list' : objects, 'category' : category})

"""class browseSupply(ListView):
	model = Supply

	def get_queryset(self):
		self.category = self.kwargs['category']
		return Supply.objects.filter(category=self.category)"""

def addItem(request):
	selected_supply = Supply.objects.get(pk=request.POST['supplyID'])
	qty = request.POST['qty']
	try:
		current_order = Order.objects.filter(owner=1).get(status="pre-place")
	except Order.DoesNotExist:
		current_order = Order.objects.create(owner=ClinicManager.objects.get(pk=1), status="pre-place")
	order_detail = OrderDetail.objects.create(orderID=current_order, supplyID=selected_supply, quantity=qty)
	return HttpResponseRedirect(reverse('ASP:browse'))

def checkout(request):
	try:
		current_order = Order.objects.filter(owner=1).get(status="pre-place")
	except Order.DoesNotExist:
		return HttpResponse("Your current order is empty<br><a href=\"browse\">Go back</a>")
	else:
		items = OrderDetail.objects.filter(orderID=current_order)
		template_name = 'ASP/checkout.html'
		order_details = []
		for item in items:
			weight = item.supplyID.weight * item.quantity
			order_details.append((item, weight))
		return render(request, template_name, {'order_details': order_details, 'current_order': current_order})

def placeOrder(request):
	order_id = request.POST['orderID']
	priority = request.POST['priority']
	try:
		current_order = Order.objects.get(pk=order_id)
	except Order.DoesNotExist:
		return HttpResponse("Error, could not place order")
	else:
		current_order.priority = priority
		current_order.status = "Queued for Processing"
		current_order.placeTime = datetime.now()
		current_order.save()
		return HttpResponse("Order placed!<br><a href=\"browse\">Go back</a>")

def dispatcherView(request):
		orders = Order.objects.filter(status="Queued for Processing")
		if not orders:
			orders = Order.objects.filter(status="Queued for dispatch")
			if not orders:
				return HttpResponse("There is currently no order.<br><a href=\"dispatcherView\">Refresh</a>")
		priority_queue = []
		for order in orders:
			heappush(priority_queue, order)
		print(priority_queue)
		next_drone_orders = []
		weight_limit = Decimal(25.00)
		current_weight = Decimal(0.00)
		while priority_queue:
			next_order = heappop(priority_queue)
			order_weight = Decimal(0.00)
			for item in OrderDetail.objects.filter(orderID=next_order):
				order_weight +=  item.quantity * item.supplyID.weight
			order_weight += Decimal(1.20)
			if current_weight + order_weight > weight_limit:
				break
			else:
				next_drone_orders.append(next_order)
				current_weight += order_weight
		template_name = 'ASP/dispatcher_view.html'
		return render(request, template_name, {'next_drone_orders': next_drone_orders})

def getDispatcherAction(request):
	orders = request.POST.getlist('order')	#orders here is a list of order id

	if request.POST.get('csv', False):
		response = getCSV(orders)
		return response
	else:
		updateStatuses(orders)
		return HttpResponse("All order statuses have been updated<br><a href=\"dispatcherView\">Go back</a>")

def getCSV(orders):
	clinics = []
	for orderID in orders:
		order = Order.objects.get(pk=orderID)
		clinic = order.owner.clinic
		if clinic not in clinics:
			clinics.append(clinic)
	route = getRoute(clinics)
	route.pop(0)
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="itinerary.csv"'
	writer = csv.writer(response)
	for location in route:
		writer.writerow([location.latitude, location.longitude, location.altitude])
	return response

def updateStatuses(orders):
	for orderID in orders:
		order = Order.objects.get(pk=orderID)
		order.status = "Dispatched"
		order.dispatchTime = datetime.now()
		order.save()
	return

def getRoute(clinics):	#clinics should be a list of clinic object
	frontier = []
	numOfStates = len(clinics)
	startState = Clinic.objects.get(name="Queen Mary Hospital Drone Port")
	heappush(frontier, (Decimal(0.00), [startState]))
	while frontier:
		node = heappop(frontier)
		if isGoalState(node[1], numOfStates):
			return node[1]
		if len(node[1]) > numOfStates:
			clinic1 = node[1][-1]
			distance = DistanceBetweenClinic.objects.get(clinic1=clinic1, clinic2=startState)
			heappush(frontier, (node[0]+distance.distance, node[1]+[startState]))
		else:
			for clinic in clinics:	#id version: clinic_id in clinics:
				if clinic not in node[1]:
					clinic1 = node[1][-1]
					clinic2 = clinic
					try:
						distance = DistanceBetweenClinic.objects.get(clinic1=clinic1, clinic2=clinic2)
					except DistanceBetweenClinic.DoesNotExist:
						distance = DistanceBetweenClinic.objects.get(clinic1=clinic2, clinic2=clinic1)
					heappush(frontier, (node[0]+distance.distance, node[1]+[clinic2]))

def isGoalState(stateSequence, numOfStates):
	print("stateSequence: ", stateSequence)
	if len(stateSequence) > numOfStates+1:
		return True
	else:
		return False
