from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from heapq import heappush, heappop
from decimal import *
import csv

from ASP.models import *

def dispatcherView(request):
	orders = Order.objects.filter(status="Queued for Dispatch")
	if not orders:
		return HttpResponse("There is currently no order.<br><a href=\"dispatcherView\">Refresh</a>")
	priority_queue = []
	for order in orders:
		heappush(priority_queue, order)
	next_drone_orders = []
	weight_limit = Decimal('25.00')
	current_weight = Decimal('0.00')
	while priority_queue:
		next_order = heappop(priority_queue)
		order_weight = next_order.weight
		if current_weight + order_weight > weight_limit:
			print("Current weight:", current_weight)
			print("next_order_weight:", order_weight)
			break
		else:
			next_drone_orders.append(next_order)
			current_weight += order_weight
	template_name = 'ASP/dispatcher_view.html'
	return render(request, template_name, {'next_drone_orders': next_drone_orders})

def getDispatcherAction(request):
	orders = request.POST.getlist('order')

	if request.POST.get('csv', False):
		response = getCSV(orders)
		return response
	else:
		updateStatuses(orders)
		return HttpResponse("All order statuses have been updated<br><a href=\"dispatcherView\">Go back</a>")

def getCSV(orders):
	locations = []
	for order_id in orders:
		order = Order.objects.get(pk=order_id)
		location = order.location
		found = False
		for _location, orders in locations:
			if location == _location:
				orders.append(order)
				found = True
				break
		if not found:
			locations.append((location,[order]))
	result = getRoute(locations)
	print("result:", result)
	route = []
	home = result.pop()
	for location, orders in result:
		route.append(location)
		print("location:", location.name, " orders:", orders)
	route.append(home)
	print(route)
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="itinerary.csv"'
	writer = csv.writer(response)
	for location in route:
		writer.writerow([location.latitude, location.longitude, location.altitude])
	return response

def updateStatuses(orders):
	clinic_managers = []
	for order_id in orders:
		order = Order.objects.get(pk=order_id)
		order.status = "Dispatched"
		order.dispatchTime = datetime.now()
		order.save()
		found = False
		for user, order_list in clinic_managers:
			if order.owner == user:
				found = True
				order_list.append(order_id)
				break
		if not found:
			clinic_managers.append((order.owner, [order_id]))
	for clinic_manager, order_list in clinic_managers:
		email = clinic_manager.user.email
		print("Dispatch notification to email: ",email)
		print("PDFs for your orders:")
		for order in order_list:
			link = "'127.0.0.1:8000/ASP/shippingLabel/"+str(order)+"'"
			print(link)
		print("\n")
	return

def getRoute(locations):	#[(location, [order1, order2]), ...]
	frontier = []
	numOfStates = len(locations)
	startState = Location.objects.get(name="Queen Mary Hospital Drone Port")
	heappush(frontier, (Decimal('0.00'), [(startState, [])]))
	shortest = 99999999999999999
	results = []	#[(location1, [order1, order2]), (location2, [order3]), ...]
	while frontier:
		node = heappop(frontier)
		if isGoalState(node[1], numOfStates):
			if node[0] < shortest:
				shortest = node[0]
				node[1].pop(0)
				results = [node[1]]
			elif node[0] == shortest:
				node[1].pop(0)
				results.append(node[1])
			else:
				for location_index in range(numOfStates):
					tiebreaker = []
					for result in results:
						location = result[location_index][0]
						orders = result[location_index][1]
						high = 0
						medium = 0
						low = 0
						for order in orders:
							priority = order.priority
							if priority == "High":
								high += 1
							elif priority == "Medium":
								medium += 1
							elif priority == "Low":
								low += 1
						tiebreaker.append((high, medium, low))
					highest = (0,0,0)
					highest_index = 0
					tie_count = 0
					for i, tie in enumerate(tiebreaker):
						if tie > highest:
							highest = tie
							highest_index = i
							tie_count = 0
						elif tie == highest:
							tie_count = 1
					if tie_count == 0:
						return results[highest_index]
				#all locations have same priority
				return results[0]
		elif len(node[1]) > numOfStates:
			location1 = node[1][-1][0]
			distance = DistanceBetweenLocation.objects.get(location1=location1, location2=startState)
			heappush(frontier, (node[0]+distance.distance, node[1]+[startState]))
		else:
			for location, orders in locations:
				if (location, orders) not in node[1]:
					location1 = node[1][-1][0]
					location2 = location
					try:
						distance = DistanceBetweenLocation.objects.get(location1=location1, location2=location2)
					except DistanceBetweenLocation.DoesNotExist:
						distance = DistanceBetweenLocation.objects.get(location1=location2, location2=location1)
					heappush(frontier, (node[0]+distance.distance, node[1]+[(location2, orders)]))
	return results

def isGoalState(stateSequence, numOfStates):
	if len(stateSequence) > numOfStates+1:
		return True
	else:
		return False