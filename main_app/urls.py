from django.urls import path, reverse_lazy
from . import views
from .Controllers.Login_Controller import Login_Controller
from .Controllers.Register_Controller import Register_Controller
from .Controllers.Company_Process_Controller import Company_Process_Controller
from .Controllers.Company_Controller import Company_Controller
from .Controllers.Order_Controller import Order_Controller
from .Controllers.Company_Client_Controller import Company_Client_Controller
from .Controllers.Client_Order_Controller import Client_Order_Controller
from .Controllers.Steps_Template_Controller import Steps_Template_Controller
from .Controllers.Orders_Maintanance_Controller import Orders_Maintanance_Controller



app_name = "main_app"

urlpatterns = [
    path('', views.main_page, name='Main_page'),
    path('orders_manager/login/', Login_Controller.as_view(), name = 'Login'),
    path('orders_manager/register/', Register_Controller.as_view(), name = 'Register'),
    path('orders_manager/processes_maintenance/', Company_Process_Controller.as_view(), name = 'create_process'),
    path('orders_manager/create_company/', Company_Controller.as_view(), name = 'create_company'),
    path('orders_manager/create_order/', Order_Controller.as_view(), name = 'order_controller'),
    path('orders_manager/clients_maintenance/', Company_Client_Controller.as_view(), name = 'client_controller'),
    path('orders_manager/order_details/', Client_Order_Controller.as_view(), name = 'Client_Order_Controller'),
    path('orders_manager/steps_template/', Steps_Template_Controller.as_view(), name = 'Steps_Template_Controller'),
    path('orders_manager/orders_maintenance/', Orders_Maintanance_Controller.as_view(), name = 'Orders_Maintanance_controller'),
]




