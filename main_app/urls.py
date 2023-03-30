from django.urls import path
from . import views
from .Controllers.Login_Controller import Login_Controller
from .Controllers.Register_Controller import Register_Controller
from .Controllers.Company_Process_Controller import Company_Process_Controller
from .Controllers.Company_Controller import Company_Controller
from .Controllers.Order_Controller import Order_Controller
from .Controllers.Company_Client_Controller import Company_Client_Controller
from .Controllers.Client_Order_Controller import Client_Order_Controller



app_name = "main_app"

urlpatterns = [
    path('order_tracking/', views.members, name='members'),
    path('registration_test/', views.registration_example, name='registration_example'),
    path('login_test/', views.login_example, name='login_example'),
    path('login/', Login_Controller.as_view(), name = 'Login'),
    path('register/', Register_Controller.as_view(), name = 'Register'),
    path('create_process/', Company_Process_Controller.as_view(), name = 'create_process'),
    path('create_company/', Company_Controller.as_view(), name = 'create_company'),
    path('create_order/', Order_Controller.as_view(), name = 'order_controller'),
    path('users/', Company_Client_Controller.as_view(), name = 'client_controller'),
    path('order_details/', Client_Order_Controller.as_view(), name = 'Client_Order_Controller'),
]




