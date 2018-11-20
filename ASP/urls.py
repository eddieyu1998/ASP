from django.urls import path
from . import views

app_name = 'ASP'
urlpatterns = [
	path('', views.DefaultView, name='DefaultView'),
	path('browse', views.browse.as_view(), name='browse'),
	#path('browse/<int:user>', views.browse.as_view(), name='browse'),
	path('addItem', views.addItem, name='addItem'),
	path('checkout', views.checkout, name='checkout'),
	path('placeOrder', views.placeOrder, name='placeOrder'),
	path('resetOrder', views.resetOrder, name='resetOrder'),
	path('dispatcherView', views.dispatcherView, name='dispatcherView'),
	path('getDispatcherAction', views.getDispatcherAction, name="getDispatcherAction"),
	path('warehouseView', views.warehouseView, name='warehouseView'),
	path('removeTop', views.removeTopForProcess, name='removeTopForProcess'),
	path('process', views.process, name='process'),
	path('admin', views.admin, name='admin'),
	path('sendToken', views.sendToken, name='sendToken'),
	path('registration/<int:id>', views.registration, name='registration'),
	path('addInvitation', views.addInvitation, name='addInvitation'),
]
