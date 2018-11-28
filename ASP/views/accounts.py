from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as d_logout, update_session_auth_hash
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from ASP.forms import RegistrationForm, UpdateInfoForm
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

def account(request):
	user = request.user
	if request.method == "POST":
		form = UpdateInfoForm(request.POST, instance=user)
		if form.is_valid:
			form.save()
			messages.success(request, "Info updated")
			return HttpResponseRedirect(reverse('ASP:account'))
	else:
		form = UpdateInfoForm(instance=request.user)

	if user.groups.filter(name="Clinic Manager").count():
		role = "Clinic Manager"
	elif user.groups.filter(name="Warehouse Personnel").count():
		role = "Warehouse Personnel"
	elif user.groups.filter(name="Dispatcher").count():
		role = "Dispatcher"
	template_name = "ASP/account.html"
	return render(request, template_name, {'form': form, 'role': role})

def changePassword(request):
	user = request.user
	form = PasswordChangeForm(user=request.user)
	template_name = "ASP/change_password.html"
	return render(request, template_name, {'form': form})

def passwordSuccess(request):
	user = request.user
	form = PasswordChangeForm(request.user, request.POST)
	if form.is_valid():
		user = form.save()
		update_session_auth_hash(request, user)
		messages.success(request, "Password updated")
		return HttpResponseRedirect(reverse('ASP:account'))
	else:
		template_name = "ASP/change_password.html"
		return render(request, template_name, {'form': form})

def logout(request):
	d_logout(request)
	return HttpResponseRedirect(reverse('login'))
