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


from main_app.models import (
    Company,
    Mapping_Usuario_Empresa,
    Company_Client, 
    Company_Order, 
    Process_Step_Client,
    Company_Process_step_template
    )


class Orders_Maintanance_Controller(APIView):

    def get(self, request):
        template = loader.get_template('Orders_Maintenance.html')
        session = request.COOKIES.get("sessionid","")
        try:
            data = prepare_data(session)
        except:
            print("Unable to get data on Orders_Maintanance_Controller")
            data = {}

        if (data is None):
             return redirect('main_app:Login')

        return HttpResponse(template.render(data, request))
    
    def post(self, request):
        pass

    def put(self, request):
        pass
    

    def delete(self, request):
        pass

def sort_function(e):
    return e["Date_Received"]

def prepare_data(session):
    if(session == "" or session is None):
        #Return none. So controller can redirect
        return None
    
    company = get_company_by_session(session)

    company_orders = list(Company_Order.objects.filter(Company_id = company["id"]).values())

    orders = []
    company_orders.sort(key=sort_function, reverse=True)
    
    for order in company_orders:
        client_obj = Company_Client.objects.get(id = order["Client_id"])
        client_processes = list(Process_Step_Client.objects.filter(Order_id = order["id"]).values())

        #find actual status
        status_now = None

        for process in client_processes:
            process_description_obj = Company_Process_step_template.objects.get(id = process["Company_Process_step_template_id"])
            if status_now is None:
                status_now = set_status_now(process, process_description_obj)
            elif status_now["Status"] == "Complete" and int(process_description_obj.Step_Order_Number) > int(status_now["Step_Order_Number"] ):
                status_now = set_status_now(process, process_description_obj)
            elif status_now["Status"] == "Pending" and int(process_description_obj.Step_Order_Number) < int(status_now["Step_Order_Number"] ) and process["Status"] == "Complete":
                status_now = set_status_now(process, process_description_obj)

        orders.append({
            "id" : order["id"],
            "Date_Received" : order["Date_Received"],
            "Description" : order["Description"],
            "Order_Status" : order["Status"],
            "Client_name" : client_obj.Name,
            "Client_Address" : client_obj.Address,
            "Client_Phone" : client_obj.Cellphone,
            "Client_Email" : client_obj.Email,
            "Step_Info" : status_now
        })
    return {
        "company_orders": orders
    }

def change_order_new_step(json_data):
    #json_data["order_id"]
    order = Company_Order.objects.get(id = json_data["order_id"])

    client_processes = list(Process_Step_Client.objects.filter(Order_id = json_data["order_id"]).values())
    
    next_step_id = None
    these_step_id = None

    for process in client_processes:
        process_description_obj = Company_Process_step_template.objects.get(id = process["Company_Process_step_template_id"])
        if process["Status"] == "Complete":
            pass
        elif process["Status"] == "Pending" and these_step_id is not None:
            if int(process_description_obj.Step_Order_Number) < int(these_step_id["order"] ):
                next_step_id =  these_step_id
                these_step_id =  { "id" : process["id"] , "order" : process_description_obj.Step_Order_Number}
            elif int(process_description_obj.Step_Order_Number) > int(these_step_id["order"] ) and next_step_id is None:
                next_step_id =  { "id" : process["id"] , "order" : process_description_obj.Step_Order_Number}
            elif next_step_id is None and int(process_description_obj.Step_Order_Number) < int(next_step_id["order"] ):
                next_step_id =  { "id" : process["id"] , "order" : process_description_obj.Step_Order_Number}
        elif process["Status"] == "Pending" and these_step_id is None:
            these_step_id =  { "id" : process["id"] , "order" : process_description_obj.Step_Order_Number}

    if these_step_id is None:
        #This means the last status was already Complete
        return None
    elif next_step_id is None and these_step_id is not None:
        #Means these step is the final so order status is moved to "closed"
        actual_process = Process_Step_Client.objects.get(id = these_step_id["id"])
        actual_process.Status = "Complete"
        actual_process.save()
        order.Status = "Closed"
        order.save()
        return "Done"
    else:
        #Only modify the client step
        actual_process = Process_Step_Client.objects.get(id = these_step_id["id"])
        actual_process.Status = "Complete"
        actual_process.save()
        return "Done"

def set_status_now(process, description_obj):
    return {
        "id" : process["id"],
        "Notes" : process["Notes"],
        "Status" : process["Status"],
        "Step_Name" : description_obj.Step_Name,
        "Step_Order_Number" : description_obj.Step_Order_Number,
        "Description" : description_obj.Description
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