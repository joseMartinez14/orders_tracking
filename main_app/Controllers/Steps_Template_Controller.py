import json

from rest_framework.views import APIView
from django.http import HttpResponse
from django.template import loader
from main_app.config import get_server_host
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User as auth_user


from main_app.models import Company, Mapping_Usuario_Empresa, Company_Client, Company_Process_step_template


class Steps_Template_Controller(APIView):

    def get(self, request):
        pass
    
    def post(self, request):
        session = request.COOKIES.get("sessionid","")
        x = json.loads(list(request.data.dict().keys())[0])

        try:
            result = get_steps_template(x)
            return Response(result, status=status.HTTP_200_OK)
        except:
            print("An exception occurred") 
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        pass
    

    def delete(self, request):
        pass



def get_steps_template(json_data):
    return Company_Process_step_template.objects.filter(Company_Process_id = json_data["process_id"]).values()


def update_company_client(json_data):
    client = Company_Client.objects.get(id = json_data["client_id"])

    client.Name = json_data["client_name"]
    client.Cellphone = json_data["client_cellphone"]
    client.Email = json_data["client_email"]
    client.Address = json_data["client_address"]

    client.save()


def delete_company_client(json_data):
    Company_Client.objects.filter(id = json_data["client_id"]).delete()


def create_company_client(json_data, session):
    if(session == "" or session is None):
        #Return none. So controller can redirect
        return None
    company = get_company_by_session(session)
    if(company is None):
        print("Company is None")
        print(company)
        return "UNAVAILABLE"
    
    _user = get_user_by_session(session)

    if not verify_client(json_data["client_email"], company["id"]):
        return "EXISTS"

    company_user = Company_Client(
        Name = json_data["client_name"],
        Cellphone = json_data["client_cellphone"],
        Email = json_data["client_email"],
        Address = json_data["client_address"],
        Company_id = company["id"]
    )

    company_user.save()

    return company_user


def verify_client(client_email, company_id):
    try:
        client = Company_Client.objects.filter(Email = client_email, Company_id = company_id)
        if not client:
            return True
        return False
    except:
        return True

def prepare_data(session):
    if(session == "" or session is None):
        #Return none. So controller can redirect
        return None
    
    company_clients = []

    company = get_company_by_session(session)

    try:
        company_clients = list(Company_Client.objects.filter(Company_id = company["id"]).values())
    except:
        company_clients = None

    return {
        "company_clients": company_clients
    }


    
def get_user_by_session(session):
    print("aqui aquiu aqui")
    print(session)
    s = Session.objects.get(pk=session)
    user_logged_in = s.get_decoded()
    user_id = user_logged_in["_auth_user_id"]
    _user = auth_user.objects.filter(id=user_id)
    return user_id

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