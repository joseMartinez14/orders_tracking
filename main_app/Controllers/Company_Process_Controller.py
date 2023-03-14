import json

from rest_framework.views import APIView
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.db import connections
from django.db import connection
from django.template import loader
from main_app.config import get_server_host, get_user_by_session
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from django.shortcuts import redirect
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User as auth_user

from main_app.models import Company,Mapping_Usuario_Empresa, Company_Process, Company_Process_step_template


class Company_Process_Controller(APIView):

    def get(self, request):
        #I guess I need to check cache and to see if is logged in or session?
        template = loader.get_template('Company_Process.html')
        session = request.COOKIES.get("sessionid","")
        data = prepare_data(session)
        if (data is None):
             return redirect('main_app:Login')
        return HttpResponse(template.render(data, request))
    
    def post(self, request):
        pass

    def put(self, request):
        print("Got to post on Register_Controller put")
        session = request.COOKIES.get("sessionid","")
        x = json.loads(request.body)
        print("This is the body")
        print(x)
        
        result = insert_process(x, session)
    
        try:
            if (result is None):
                return redirect('main_app:Login')
            elif(result == "COMPANY_UNAVAILABLE"):
                return Response({}, status=status.HTTP_302_FOUND) 
            return Response({}, status=status.HTTP_200_OK)
        except:
            print("An exception occurred") 
            return Response({}, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request):
        pass


def insert_process(json_data, session):
    #First look up for user and then company user mapping. To know
    #if it has the permissions.
    #For testing I am going to use 1 single testing company

    if(session == "" or session is None):
        #Return none. So controller can redirect
        return None
    
    s = Session.objects.get(pk=session)
    user_logged_in = s.get_decoded()
    user_id = user_logged_in["_auth_user_id"]

    try:
        mapping = Mapping_Usuario_Empresa.objects.filter(User_id = user_id).values()
        company_id = mapping[0]["Company_id"]
        print("company_id")
        print(company_id)
        company = Company.objects.filter(id = company_id).values()[0]
    except:
        return "COMPANY_UNAVAILABLE"
    
    print(company)
    
    company_process = Company_Process(
        Process_Name = json_data["process_name"],
        Description = json_data["process_description"],
        Company_id = company["id"]
    )

    company_process.save()

    for step in json_data["steps"]:
        print(step)
        temp_step = Company_Process_step_template(
            Step_Name = step["step_name"],
            Description = step["description"],
            Step_Order_Number = step["step_Order_Number"],
            Company_Process = company_process
        )

        temp_step.save()
    
    return "GOOD"



def prepare_data(session):
    if(session == "" or session is None):
        #Return none. So controller can redirect
        return None
    
    s = Session.objects.get(pk=session)
    user_logged_in = s.get_decoded()
    user_id = user_logged_in["_auth_user_id"]
    print(user_logged_in["_auth_user_id"])
    if (user_logged_in != None):
        host = get_server_host()
        return {
            "server" : host,
            "current_user" : user_logged_in
        }
    return None
