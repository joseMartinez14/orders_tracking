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

from main_app.models import Company,Mapping_Usuario_Empresa, Company_Process, Company_Process_step_template, Company_Order


class Company_Process_Controller(APIView):

    def get(self, request):
        #I guess I need to check cache and to see if is logged in or session?
        template = loader.get_template('Company_Process_CRUD.html')
        session = request.COOKIES.get("sessionid","")
        data = prepare_data(session)
        if (data is None):
             return redirect('main_app:Login')
        return HttpResponse(template.render(data, request))
    
    def post(self, request):
        session = request.COOKIES.get("sessionid","")
        x = json.loads(list(request.data.dict().keys())[0])
        try:
            result = insert_process(x, session)
            if (result is None):
                return redirect('main_app:Login')
            elif(result == "COMPANY_UNAVAILABLE"):
                return Response({}, status=status.HTTP_302_FOUND) 
            return Response({}, status=status.HTTP_200_OK)
        except:
            print("An exception occurred") 
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        print("Got to post on Register_Controller put")
        x = json.loads(request.body)
        print("This is the body")
        print(x)
        update_process(x)
        try:
            return Response({}, status=status.HTTP_200_OK)
        except:
            print("An exception occurred") 
            return Response({}, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request):
        x = json.loads(request.body)
        try:
            if not confirm_save_delete(x):
                return Response({}, status=status.HTTP_302_FOUND)
            delete_process(x)
            return Response({}, status=status.HTTP_200_OK)
        except:
            print("An exception occurred") 
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


def confirm_save_delete(json_data):
    try:
        fake = Company_Order.objects.filter(Company_Process_id = json_data["process_id"]).values()
        return False
    except:
        return True

def delete_process(json_data):
    Company_Process.objects.filter(id = json_data["process_id"]).delete()

def update_process(json_data):
    
    process = Company_Process.objects.get(id = json_data["process_id"])

    process.Process_Name = json_data["process_name"]
    process.Description = json_data["process_description"]

    process.save()

    old_steps = []
    try:
        old_steps = list(Company_Process_step_template.objects.filter(Company_Process_id = json_data["process_id"] ).values())
    except:
        old_steps = []
    for step in json_data["steps"]:
        if step["step_id"] == -1:
            add_step = Company_Process_step_template(
                Step_Name = step["step_name"],
                Description = step["description"],
                Step_Order_Number = step["step_Order_Number"],
                Company_Process_id = json_data["process_id"]
            )
            add_step.save()
        else:
            temp_step = Company_Process_step_template.objects.get(id = step["step_id"])
            temp_step.Step_Name = step["step_name"]
            temp_step.Description = step["description"]
            temp_step.Step_Order_Number = step["step_Order_Number"]
            temp_step.save()
        for old_step in old_steps:
            if old_step["id"] == step["step_id"]:
                print("quiero borrar")
                print(old_step)
                old_steps.remove(old_step)

        temp_step.save()
    
    #Delete remaining steps, because it means client delete those

    for old_step in old_steps:
        Company_Process_step_template.objects.filter(id = old_step["id"]).delete()
    


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
    
    company_process = []
    company_process_steps = []

    company = get_company_by_session(session)
    
    try:
        company_process = list(Company_Process.objects.filter(Company_id = company["id"]).values() )
    except:
        company_process = None

    if company_process is not None:
        for process in company_process:
            temp_list = []
            try:
                temp_list = list(Company_Process_step_template.objects.filter(Company_Process_id = process["id"]).values() )
            except:
                temp_list = []
            company_process_steps.extend(temp_list)

    return {
        "company_process" : company_process,
        "company_process_steps" : company_process_steps
    }




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
