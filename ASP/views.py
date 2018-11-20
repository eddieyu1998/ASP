from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from heapq import heappush, heappop
from decimal import *
import csv
import reportlab	#for generating PDF, please run "pip install reportlab" in the virtual env
from reportlab.pdfgen import canvas
import io

from ASP.models import *

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
		total_weight = 0
		message= "OVERWEIGHT. Please Reset Order"
		items = OrderDetail.objects.filter(orderID=current_order)
		template_name = 'ASP/checkout.html'
		order_details = []
		for item in items:
			weight = item.supplyID.weight * item.quantity
			order_details.append((item, weight))
			total_weight +=weight
		total_weight= float(total_weight)+1.2
		if total_weight <25:
		    return render(request, template_name, {'order_details': order_details, 'current_order': current_order,'Total_Weight': round(total_weight,2)})
		else:
			return render(request, template_name, {'order_details': order_details, 'current_order': current_order,'Total_Weight': message})

  

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

def resetOrder(request):
	ord = Order.objects.filter(owner=1).get(status="pre-place")
	ord.delete()
	return HttpResponse("Your order has been removed!<br><a href=\"browse\">Go back</a>")

def dispatcherView(request):
	orders = Order.objects.filter(status="Queued for Dispatch")
	if not orders:
		return HttpResponse("There is currently no order.<br><a href=\"dispatcherView\">Refresh</a>")
	priority_queue = []
	for order in orders:
		heappush(priority_queue, order)
	#print(priority_queue)
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


def warehouseView(request):
	orders = Order.objects.filter(status="Queued for Processing")
	template_name = 'ASP/warehouse_view.html'
	if not orders:
		return render(request, template_name, {'top_order': [], 'orders': []})
	priority_queue = []
	for order in orders:
		heappush(priority_queue, order)
	top_order = heappop(priority_queue)
	return render(request, template_name, {'top_order': top_order, 'orders': priority_queue})

def removeTopForProcess(request):
	top_order = Order.objects.get(pk=request.POST['orderID'])
	top_order.status = "Processing by Warehouse"
	top_order.save()
	return HttpResponseRedirect(reverse('ASP:warehouseView'))

def process(request):
	orders = Order.objects.filter(status="Processing by Warehouse")
	if not orders:
		return HttpResponse("<a href=\"warehouseView\">Return, no orders to be processed</a>")
	priority_queue = []
	for order in orders:
		details = order.orderdetail_set.all()
		location = order.owner.clinic.name
		heappush(priority_queue, (order, location, details))
	print(priority_queue)
	template_name = "ASP/process.html"
	return render(request, template_name, {'orders': priority_queue})

def admin(request):
	invitations = Invitation.objects.all()
	template_name = "ASP/admin.html"
	return render(request, template_name, {'invitations': invitations})

def addInvitation(request):
	email = request.POST['email']
	role = request.POST['role']
	Invitation.objects.create(email=email, role=role)
	return HttpResponseRedirect(reverse('ASP:admin'))

def sendToken(request):
	invitation_id = request.POST['invitationID']
	invitation = Invitation.objects.get(pk=invitation_id)
	email = "\""+invitation.email+"\""
	link = "\"127.0.0.1:8000/ASP/registration/"+str(invitation_id)+"\""
	print("\ntoken", link, "sent to email address", email, "\n")
	return HttpResponseRedirect(reverse('ASP:admin'))

def registration(request, invitation_id):
	try:
		invitation = Invitation.objects.get(pk=invitation_id)
	except Invitation.DoesNotExist:
		return HttpResponse("Error, token invalid!")
	else:
		email = invitation.email
		role = invitation.role
		template_name = "ASP/registration.html"
		return render(request, template_name, {'email': email, 'role': role})

def registerUser(request):
	email = request.POST['email']
	firstName = request.POST['firstName']
	lastName = request.POST['lastName']
	username = request.POST['username']
	password = request.POST['password']
	role = request.POST['role']
	clinic = request.POST.get('clinicName', False)
	if role == "Clinic Manager":
		try:
			location = Location.objects.get(name=clinic)
		except Location.DoesNotExist:
			return HttpResponse("Error, clinic not found")
		else:
			clinic_manager = ClinicManager.objects.create(firstName=firstName, lastName=lastName, username= username, password=password, email=email)
			clinic = Clinic.objects.create(manager=clinic_manager, name=clinic, latitude=location.latitude, longitude=location.longitude, altitude=location.altitude)
	elif role == "Warehouse Personnel":
		warehouse_personnel = WarehousePersonnel.objects.create(firstName=firstName, lastName=lastName, username= username, password=password, email=email)
	elif role == "Dispatcher":
		dispatcher = Dispatcher.objects.create(firstName=firstName, lastName=lastName, username= username, password=password, email=email)
	else:
		print(role)
		return HttpResponse("Error, cannot register")
	invitation = Invitation.objects.filter(email=email).delete()
	return HttpResponse("Registration success")

def getWarehouseAction(request):
	order_id = request.POST['orderID']
	location = request.POST['location']
	if request.POST.get('getShippingLabel', False):
		names = request.POST.getlist('supplyName')
		quantity = request.POST.getlist('quantity')
		details = zip(names, quantity)
		response = getShippingLabel(order_id, location, details)
		return response
	else:
		warehouseUpdateStatuses(order_id)
		return HttpResponse("Order status have been updated<br><a href=\"process\">Go back</a>")

def getShippingLabel(order_id, location, details):
	buffer = io.BytesIO()
	p = canvas.Canvas(buffer)
	p.drawString(80, 800, "order id: "+str(order_id))
	p.drawString(80, 775, "location: "+location)
	p.drawString(80, 725, "list of items:")
	y = 700
	for detail in details:
		p.drawString(80, y, detail[0]+": "+str(detail[1]))
		y -= 25
	p.showPage()
	p.save()
	pdf = buffer.getvalue()
	buffer.close()
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="shippinglabel.pdf"'
	response.write(pdf)
	return response

def warehouseUpdateStatuses(order_id):
	order = Order.objects.get(pk=order_id)
	order.status = "Queued for Dispatch"
	order.save()
	return