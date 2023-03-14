import json

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


from main_app.models import Company, Mapping_Usuario_Empresa, Company_Process, Company_Client


class Order_Controller(APIView):

    def get(self, request):
        #I guess I need to check cache and to see if is logged in or session?
        template = loader.get_template('New_Order.html')
        session = request.COOKIES.get("sessionid","")
        data = prepare_data(session)
        if (data is None):
             return redirect('main_app:Login')
        return HttpResponse(template.render(data, request))
    
    def post(self, request):
        pass

    def put(self, request):
        print("Got to post on Order_Controller put")
        session = request.COOKIES.get("sessionid","")
        x = json.loads(request.body)
        print("This is the body")
        print(x)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request):
        pass


def prepare_data(session):
    if(session == "" or session is None):
        #Return none. So controller can redirect
        return None
    
    company = None
    company_process = None
    company_clients = None

    try:
        company = get_company_by_session(session)
    except:
        return "COMPANY_UNABLE" 

    print(company)

    #Necesito las procesos por compañia y los clientes por compañia

    try:
        company_process = Company_Process.objects.filter(Company_id = company["id"]).values()
    except:
        company_process = []

    try:
        company_clients = Company_Client.objects.filter(Company_id = company["id"]).values()
    except:
        company_clients = []

    print("company_process")
    print(company_process)
    print("company_clients")
    print(company_clients)

    host = get_server_host()
    return {
        "server" : host,
        "company_process" : list(company_process),
        "company_clients" : list(company_clients)
    }
    return None

    
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


