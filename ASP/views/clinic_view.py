from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from decimal import *

from ASP.models import *

def browse(request):
	user = request.user
	clinic_manager = ClinicManager.objects.get(user=user)
	category = request.POST.get('category', False)
	search = request.POST.get('search', False)
	if search:
		if not category or category == "all":
			objects = Supply.objects.filter(name__contains=search)
		else:
			objects = Supply.objects.filter(category=category, name__contains=search)
	elif not category or category == "all":
		objects = Supply.objects.all()
	else:
		objects = Supply.objects.filter(category=category)
	print(objects)
	template_name = 'ASP/supply_list.html'
	return render(request, template_name, {'object_list' : objects, 'category' : category})

def addItem(request):
	user = request.user
	clinic_manager = ClinicManager.objects.get(user=user)
	selected_supply = Supply.objects.get(pk=request.POST['supply_id'])
	qty = request.POST['qty']
	try:
		current_order = Order.objects.filter(owner=clinic_manager).get(status="pre-place")
	except Order.DoesNotExist:
		current_order = Order.objects.create(owner=clinic_manager, status="pre-place")
	try:
		previous_select = OrderDetail.objects.get(order=current_order, supply=selected_supply)
	except OrderDetail.DoesNotExist:
		order_detail = OrderDetail.objects.create(order=current_order, supply=selected_supply, quantity=qty)
	else:
		previous_select.quantity += int(qty)
		previous_select.save()
	return HttpResponseRedirect(reverse('ASP:browse'))

def checkout(request):
	user = request.user
	clinic_manager = ClinicManager.objects.get(user=user)
	try:
		current_order = Order.objects.filter(owner=clinic_manager).get(status="pre-place")
	except Order.DoesNotExist:
		return HttpResponse("Your current order is empty<br><a href=\"browse\">Go back</a>")
	else:
		items = OrderDetail.objects.filter(order=current_order)
		template_name = 'ASP/checkout.html'
		order_details = []
		total_weight = Decimal('0.00')
		for item in items:
			weight = Decimal(item.supply.weight) * item.quantity
			order_details.append((item, weight))
			total_weight += weight
		total_weight += Decimal('1.20')
		if total_weight < 25:
			return render(request, template_name, {'order_details': order_details, 'current_order': current_order,'Total_Weight': total_weight})
		else:
			return render(request, template_name, {'order_details': order_details, 'current_order': current_order,'Total_Weight': total_weight, 'overweight': True})

def changeQuantity(request):
	new_quantity = request.POST['quantity']
	order = Order.objects.get(pk=request.POST.get('order_id'))
	supply = Supply.objects.get(pk=request.POST['supply_id'])
	order_detail = OrderDetail.objects.get(order=order, supply=supply)
	order_detail.quantity = new_quantity
	order_detail.save()
	return HttpResponseRedirect('/ASP/checkout')

def placeOrder(request):
	user = request.user
	clinic_manager = ClinicManager.objects.get(user=user)
	order_id = request.POST['order_id']
	priority = request.POST['priority']
	weight = request.POST['weight']
	try:
		current_order = Order.objects.get(pk=order_id)
	except Order.DoesNotExist:
		return HttpResponse("Error, could not place order")
	else:
		current_order.priority = priority
		current_order.status = "Queued for Processing"
		current_order.weight = weight
		current_order.location = clinic_manager.clinic
		current_order.placeTime = datetime.now()
		current_order.save()
		return HttpResponse("Order placed!<br><a href=\"browse\">Go back</a>")

def resetOrder(request):
	user = request.user
	clinic_manager = ClinicManager.objects.get(user=user)
	order = Order.objects.filter(owner=clinic_manager).get(status="pre-place")
	order.delete()
	return HttpResponse("Your order has been removed!<br><a href=\"browse\">Go back</a>")

def viewOrders(request):
	user = request.user
	clinic_manager = ClinicManager.objects.get(user=user)
	orders = Order.objects.filter(owner=clinic_manager).exclude(status="Delivered")
	order_details = []
	for order in orders:
		details = order.orderdetail_set.all()
		order_details.append((order, details))
	template_name = "ASP/view_orders.html"
	return render(request, template_name, {'order_details':order_details})

def updateOrder(request):
	user = request.user
	clinic_manager = ClinicManager.objects.get(user=user)
	order_id = request.POST.get('order_id')
	try:
		order = Order.objects.get(pk=order_id, owner=clinic_manager)
	except Order.DoesNotExist:
		return HttpResponse("Error, order not found.<br><a href=\"browse\">Return</a>")
	else:
		status = request.POST.get('status')
		if status == "cancel":
			order.delete()
			return HttpResponse("Order status has been deleted.<br><a href=\"viewOrders\">Return</a>")
		elif status == "receive":
			order.status = "Delivered"
			order.deliveredTime = datetime.now()
			order.save()
			return HttpResponse("Order status has been updated to deliverd.<br><a href=\"viewOrders\">Return</a>")
