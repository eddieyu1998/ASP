from django.urls import path
from . import views

app_name = 'ASP'
urlpatterns = [
	path('loggedIn', views.loggedIn, name="loggedIn"),
	path('admin', views.admin, name='admin'),
	path('sendToken', views.sendToken, name='sendToken'),
	path('addInvitation', views.addInvitation, name='addInvitation'),
	path('registration/<int:invitation_id>', views.registration, name='registration'),
	path('registerUser', views.registerUser, name="registerUser"),
	path('account', views.account, name="account"),
	path('changePassword', views.changePassword, name="changePassword"),
	path('passwordSuccess', views.passwordSuccess, name="passwordSuccess"),

	path('browse', views.browse, name='browse'),
	path('addItem', views.addItem, name='addItem'),
	path('checkout', views.checkout, name='checkout'),
	path('placeOrder', views.placeOrder, name='placeOrder'),
	path('resetOrder', views.resetOrder, name='resetOrder'),
	path('changeQuantity', views.changeQuantity, name='changeQuantity'),
	path('delivered', views.delivered, name="delivered"),

	path('warehouseView', views.warehouseView, name='warehouseView'),
	path('removeTop', views.removeTopForProcess, name='removeTopForProcess'),
	path('process', views.process, name='process'),
	path('getWarehouseAction', views.getWarehouseAction, name="getWarehouseAction"),

	path('dispatcherView', views.dispatcherView, name='dispatcherView'),
	path('getDispatcherAction', views.getDispatcherAction, name="getDispatcherAction"),
]
