from django.urls import path
from . import views
from .Controllers.Login_Controller import Login_Controller
from .Controllers.Register_Controller import Register_Controller
from .Controllers.Company_Process_Controller import Company_Process_Controller


urlpatterns = [
    path('order_tracking/', views.members, name='members'),
    path('registration_test/', views.registration_example, name='registration_example'),
    path('login_test/', views.login_example, name='login_example'),
    path('login/', Login_Controller.as_view(), name = 'Login'),
    path('register/', Register_Controller.as_view(), name = 'Register'),
    path('create_process/', Company_Process_Controller.as_view(), name = 'create_process')

]



