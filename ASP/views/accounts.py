from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from ASP.forms import RegistrationForm
from ASP.models import *

def loggedIn(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			return HttpResponseRedirect(reverse('ASP:admin'))
		user = request.user
		if user.groups.filter(name="Clinic Manager").count():
			return HttpResponseRedirect(reverse('ASP:browse'))
		elif user.groups.filter(name="Warehouse Personnel").count():
			return HttpResponseRedirect(reverse('ASP:warehouseView'))
		elif user.groups.filter(name="Dispatcher").count():
			return HttpResponseRedirect(reverse('ASP:dispatcherView'))
	else:
		return HttpResponse("Login fail")
		
def admin(request):
	invitations = Invitation.objects.all()
	template_name = "ASP/admin.html"
	return render(request, template_name, {'invitations': invitations})

def sendToken(request):
	invitation_id = request.POST['invitationID']
	invitation = Invitation.objects.get(pk=invitation_id)
	email = "\""+invitation.email+"\""
	link = "\"127.0.0.1:8000/ASP/registration/"+str(invitation_id)+"\""
	print("\ntoken", link, "sent to email address", email, "\n")
	return HttpResponseRedirect(reverse('ASP:admin'))

def addInvitation(request):
	email = request.POST['email']
	role = request.POST['role']
	Invitation.objects.create(email=email, role=role)
	return HttpResponseRedirect(reverse('ASP:admin'))

def registration(request, invitation_id):
	try:
		invitation = Invitation.objects.get(pk=invitation_id)
	except Invitation.DoesNotExist:
		return HttpResponse("Error, token invalid!")
	else:
		email = invitation.email
		role = invitation.role
		form = RegistrationForm()
		template_name = "registration/registration.html"
		return render(request, template_name, {'invitation_id': invitation_id, 'email': email, 'role': role, 'form': form})

def registerUser(request):
	invitation_id = request.POST['invitation_id']
	email = request.POST['email']
	role = request.POST['role']
	form = RegistrationForm(request.POST)
	if form.is_valid():
		if role == "Clinic Manager":
			clinic_name = request.POST.get('clinic_name', False)
			try:
				location = Location.objects.get(name=clinic_name)
			except Location.DoesNotExist:
				return HttpResponse("Error, clinic not found")
			else:
				user = form.save()
				user.email = email
				try:
					group = Group.objects.get(name=role)
				except Group.DoesNotExist:
					group = Group.objects.create(name=role)
				user.groups.add(group)
				user.save()
				clinic_manager = ClinicManager.objects.create(user=user, clinic=location)
		else:
			user = form.save()
			user.email = email
			if role == "Warehouse Personnel":
				try:
					group = Group.objects.get(name=role)
				except Group.DoesNotExist:
					group = Group.objects.create(name=role)
				user.groups.add(group)
				user.save()
				WarehousePersonnel.objects.create(user=user)
			elif role == "Dispatcher":
				try:
					group = Group.objects.get(name=role)
				except Group.DoesNotExist:
					group = Group.objects.create(name=role)
				user.groups.add(group)
				user.save()
				Dispatcher.objects.create(user=user)
			else:
				print(role,user)
				return HttpResponse("Error, could not register.")
		invitation = Invitation.objects.filter(email=email).delete()
		return HttpResponse("<h1>Registration success</h1>")
	else:
		errors = form.errors
		template_name = "registration/registration.html"
		return render(request, template_name, {'invitation_id': invitation_id, 'email': email, 'role': role, 'form': form, 'errors': errors})
