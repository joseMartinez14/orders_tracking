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
import qrcode


from main_app.models import (
    Company,
    Mapping_Usuario_Empresa,
    Company_Process,
    Company_Client,
    Company_Order,
    Company_Process_step_template,
    Process_Step_Client
)

class Order_Controller(APIView):

    def get(self, request):
        #I guess I need to check cache and to see if is logged in or session?
        template = loader.get_template('New_Order.html')
        session = request.COOKIES.get("sessionid","")
        try:
            data = prepare_data(session)
        except ValueError:
            return redirect('main_app:create_company')
        if (data is None):
             return redirect('main_app:Login')

        return HttpResponse(template.render(data, request))
    
    def post(self, request):
        pass

    def put(self, request):
        session = request.COOKIES.get("sessionid","")
        x = json.loads(request.body)
        try:
            result = create_new_order(session, x)
            if (result is None):
                return Response({}, status=status.HTTP_307_TEMPORARY_REDIRECT)
            if (result == "COMPANY_UNAVAILABLE"):
                return Response({}, status=status.HTTP_302_FOUND)
            return Response({"order_id": result.id}, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pass

def create_new_order(session, data):
    if(session == "" or session is None):
        #Return none. So controller can redirect
        return None
    
    company = None

    try:
        company = get_company_by_session(session)
    except:
        return "COMPANY_UNAVAILABLE" 
    
    order = Company_Order(
        Date_Received = datetime.now(),
        Description = data["order_description"],
        Company_id = company["id"],
        Company_Process_id = data["process_id"],
        Client_id = data["client_id"],
        Status = "Open"
    )

    order.save()

    order_db = Company_Order.objects.get(id = order.id)
    order_db.qr_url = f"{get_server_host()}/orders_manager/order_details/?order_number={order_db.id}"
    order_db.save()
    order_db.save()

    steps = Company_Process_step_template.objects.filter(Company_Process_id=data["process_id"]).values()

    for step in sorted(steps, key=lambda x: x["Step_Order_Number"]):
        client_order_step = Process_Step_Client(
            Company_Process_step_template_id = step["id"],
            Order = order,
            Notes = "",
            Status = "Pending"
        )
        client_order_step.save()


    return order


def prepare_data(session):
    if(session == "" or session is None):
        #Return none. So controller can redirect
        return None
    
    company = None
    company_process = None
    company_clients = None

    company = get_company_by_session(session)
    if company is None:
        raise ValueError("need to create a company")
    #Necesito las procesos por compañia y los clientes por compañia
    try:
        company_process = Company_Process.objects.filter(Company_id = company["id"]).values()
    except:
        company_process = []
    try:
        company_clients = Company_Client.objects.filter(Company_id = company["id"]).values()
    except:
        company_clients = []

    host = get_server_host()
    return {
        "server" : host,
        "company_process" : list(company_process),
        "company_clients" : list(company_clients)
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

    try:
        mapping = Mapping_Usuario_Empresa.objects.filter(User_id = _user_id ).values()
        company_id = mapping[0]["Company_id"]
        company = Company.objects.filter(id = company_id).values()[0]
        return company
    except:
        return None


