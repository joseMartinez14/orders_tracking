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


from main_app.models import Company, Mapping_Usuario_Empresa


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

    
