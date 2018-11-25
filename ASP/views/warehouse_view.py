from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from heapq import heappush, heappop
from decimal import *
import reportlab	#for generating PDF, please run "pip install reportlab" in the virtual env
from reportlab.pdfgen import canvas
import io

from ASP.models import *


def warehouseView(request):
	orders = Order.objects.filter(status="Queued for Processing")
	template_name = 'ASP/warehouse_view.html'
	if not orders:
		return render(request, template_name, {'top_order': [], 'orders': []})
	priority_queue = list(orders)
	priority_queue.sort()
	top_order = priority_queue.pop(0)
	return render(request, template_name, {'top_order': top_order, 'orders': priority_queue})

def removeTopForProcess(request):
	top_order = Order.objects.get(pk=request.POST['order_id'])
	top_order.status = "Processing by Warehouse"
	top_order.save()
	return HttpResponseRedirect(reverse('ASP:warehouseView'))

def process(request):
	orders = Order.objects.filter(status="Processing by Warehouse")
	if not orders:
		return HttpResponse("<a href=\"warehouseView\">Return, no more removed orders for packing</a>")
	priority_queue = []
	for order in orders:
		details = order.orderdetail_set.all()
		location = order.location.name
		priority_queue.append((order, location, details))
	priority_queue.sort()
	template_name = "ASP/process.html"
	return render(request, template_name, {'orders': priority_queue})

def getWarehouseAction(request):
	order_id = request.POST['order_id']
	location = request.POST['location']
	if request.POST.get('getShippingLabel', False):
		names = request.POST.getlist('supply_name')
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