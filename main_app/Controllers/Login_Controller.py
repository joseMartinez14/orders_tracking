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
import os
import random
import string
from django.contrib.sessions.models import Session
from datetime import datetime
from django.contrib.auth.models import User as auth_user

from main_app.models import User,Session

from django.contrib.auth import authenticate, login

class Login_Controller(APIView):

    def get(self, request):
        #I guess I need to check cache and to see if is logged in or session?
        template = loader.get_template('Login.html')
        #template = loader.get_template('registration/password_reset_form')
        
        data = prepare_login_data()
        return HttpResponse(template.render(data, request))
    
    def post(self, request):
        print("Got to post on Test_Controller")
        x = json.loads(list(request.data.dict().keys())[0])
        print(x)
        try:
            login_user = make_login(x["usuario"], x["contrasenna"])
            if(login_user is not None):
                login(request, login_user)
                response = Response({}, status=status.HTTP_200_OK)
                return response
        except:
            print("An exception occurred") 
            return Response({}, status=status.HTTP_302_FOUND)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)    
    
    def put(self, request):
        print("This is puta")
        pass

    def delete(self, request):
        pass




def prepare_login_data():
    host = get_server_host()
    return {
        "server" : host
    }


def get_user_by_session(session):
    print("aqui aquiu aqui")
    print(session)
    s = Session.objects.get(pk=session)
    user_logged_in = s.get_decoded()
    user_id = user_logged_in["_auth_user_id"]
    _user = auth_user.objects.filter(id=user_id).get()
    return _user



def make_login( email:str, password:str ):

    data = authenticate(username=email, password=password)
    print("Siiiiiii la puta madreeee")
    return data



