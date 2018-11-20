from django.urls import path
from . import views

app_name = 'ASP'
urlpatterns = [
	path('', views.DefaultView, name='DefaultView'),
	path('browse', views.browse.as_view(), name='browse'),
	path('browse/<int:id>', views.browse.as_view(), name='browse'),
	path('addItem', views.addItem, name='addItem'),
	path('checkout', views.checkout, name='checkout'),
	path('checkout_get/<int:id>', views.checkout_get, name='checkout_get'),
	path('placeOrder', views.placeOrder, name='placeOrder'),
	path('resetOrder', views.resetOrder, name='resetOrder'),
	path('changeQuantity', views.changeQuantity, name='changeQuantity'),
	path('dispatcherView', views.dispatcherView, name='dispatcherView'),
	path('getDispatcherAction', views.getDispatcherAction, name="getDispatcherAction"),
	path('warehouseView', views.warehouseView, name='warehouseView'),
	path('removeTop', views.removeTopForProcess, name='removeTopForProcess'),
	path('process', views.process, name='process'),
	path('admin', views.admin, name='admin'),
	path('sendToken', views.sendToken, name='sendToken'),
	path('registration/<int:invitation_id>', views.registration, name='registration'),
	path('addInvitation', views.addInvitation, name='addInvitation'),
	path('registerUser', views.registerUser, name="registerUser"),
	path('getWarehouseAction', views.getWarehouseAction, name="getWarehouseAction"),
	path('registration_test', views.registration_test, name="registration_test"),
	path('login', views.login, name="login"),
]
