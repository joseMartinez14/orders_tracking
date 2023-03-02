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

from main_app.models import Company


class Company_Controller(APIView):

    def get(self, request):
        #I guess I need to check cache and to see if is logged in or session?
        template = loader.get_template('Create_Company.html')
        session = request.COOKIES.get("user_session_id","")
        data = prepare_data(session)
        if (data is None):
             return redirect('main_app:Login')
        return HttpResponse(template.render(data, request))
    
    def post(self, request):
        pass

    def put(self, request):
        print("Got to post on Company_Controller put")

        x = json.loads(request.body)
        print("This is the body")
        print(x)

        print("This is the data")
        print(request.data)

        try:
            company_process(x)
            return Response({}, status=status.HTTP_200_OK)
        except:
            print("An exception occurred") 
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request):
        pass


def company_process(json_data):

    company = Company(
        Name = json_data["company_name"],
        Description = json_data["company_name"],
        membership = True,
        Creation_date = datetime.now(),
        Last_membership_update = datetime.now()
    )
    company.save()



def prepare_data(session):
    if(session == "" or session is None):
        #Return none. So controller can redirect
        return None
    
    user_logged_in = get_user_by_session(session)
    if (user_logged_in != None):
        host = get_server_host()
        return {
            "server" : host,
            "current_user" : user_logged_in
        }
    return None
    
    
