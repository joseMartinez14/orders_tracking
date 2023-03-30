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


from main_app.models import Company, Mapping_Usuario_Empresa, Company_Client


class Company_Client_Controller(APIView):

    def get(self, request):
        pass
    
    def post(self, request):
        pass

    def put(self, request):
        print("Got to post on Company_Client_Controller put")
        session = request.COOKIES.get("sessionid","")
        x = json.loads(request.body)

        get_company_by_session(session)

        try:
            result = create_company_client(x, session)
            if (result is None):
                return redirect('main_app:Login')
            if (result == "EXISTS"):
                return Response({}, status=status.HTTP_302_FOUND)
            if (result == "UNAVAILABLE"):
                return Response({}, status=status.HTTP_307_TEMPORARY_REDIRECT)

            return Response({"client_id": result.id, "client_name": result.Name}, status=status.HTTP_200_OK)
        except:
            print("An exception occurred") 
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request):
        pass


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
    
    _user = get_user_by_session(session)

    host = get_server_host()
    return {
        "server" : host,
        "current_user" : _user
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