import json
from datetime import datetime

from rest_framework.views import APIView
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.db import connections
from django.db import connection
from django.template import loader
from main_app.config import get_server_host
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User as auth_user

from main_app.models import (
    Company,
    Mapping_Usuario_Empresa,
    Company_Process,
    Company_Client,
    Company_Order,
    Company_Process_step_template,
    Process_Step_Client,
)

class Client_Order_Controller(APIView):

    def get(self, request):
        #I guess I need to check cache and to see if is logged in or session?
        template = loader.get_template('Client_Order.html')
        session = request.COOKIES.get("sessionid","")
        order_number = ""
        try:
            print(request.query_params)
            order_number = request.query_params['order_number']
        except:
            #TODO: Return a visual that shows an error and ask for the order number
            print("Unable to find order number")
            return None
        
        data = prepare_data(order_number)

        return HttpResponse(template.render(data, request))
    
    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

def prepare_data(order_number):
    
    company = None
    order = None
    client = None
    client_steps = []
    #Necesito las procesos por compañia y los clientes por compañia
    try:
        order = Company_Order.objects.filter(id = order_number).values()[0]
    except:
        order = None
    
    if order is not None:

        try:
            company = Company.objects.filter(id = order["Company_id"]).values()[0]
        except:
            company = None

        try:
            client = Company_Client.objects.filter(id = order["Client_id"]).values()[0]
        except:
            client = None
        try:
            client_steps_db = Process_Step_Client.objects.filter(Order_id = order["id"]).values()
            for step in list(client_steps_db):
                template_info = Company_Process_step_template.objects.filter(id = step["Company_Process_step_template_id"]).values()[0]
                client_steps.append(
                    {
                        "step_name": template_info["Step_Name"],
                        "step_description": template_info["Description"],
                        "status": step["Status"],
                        "Notes": step["Notes"] 
                    }
                )
        except:
            client_steps = None

    print("************")
    print(client_steps)

    return {
        "company" : company,
        "order" : order,
        "client" : client,
        "client_steps" : client_steps
    }

    
def get_user_by_session(session):
    s = Session.objects.get(pk=session)
    user_logged_in = s.get_decoded()
    user_id = user_logged_in["_auth_user_id"]
    _user = auth_user.objects.filter(id=user_id)
    return _user


def get_company_by_session(session):
    s = Session.objects.get(pk=session)
    user_logged_in = s.get_decoded()
    _user_id = user_logged_in["_auth_user_id"]
    mapping = Mapping_Usuario_Empresa.objects.filter(User_id = _user_id ).values()
    company_id = mapping[0]["Company_id"]
    company = Company.objects.filter(id = company_id).values()[0]
    return company


