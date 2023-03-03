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
from datetime import datetime

from main_app.models import User,Session

class Login_Controller(APIView):

    def get(self, request):
        #I guess I need to check cache and to see if is logged in or session?
        template = loader.get_template('Login.html')
        #template = loader.get_template('registration/password_reset_form')
        
        data = prepare_login_data()
        return HttpResponse(template.render(data, request))
    
    def post(self, request):
        print("Got to post on Test_Controller")
        session = request.COOKIES.get("user_session_id","")
        

        if session == "":
            print("La puta session es none")
            #No se como hacer lo de la session
            print("------ generate key ---------")
            random_key = id_generator()
            session = random_key
        
        print("Esta es la fucking session")
        print(session)
        x = json.loads(list(request.data.dict().keys())[0])
        print(x)
        try:
            login_bool = make_login(x["usuario"], x["contrasenna"])
            if(login_bool):
                link_user_session(x["usuario"], session)
                response = Response({}, status=status.HTTP_200_OK)
                response.set_cookie("user_session_id", random_key)
                return response
        except:
            print("An exception occurred") 
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_302_FOUND)    
    
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


def make_login( email:str, password:str ):
    data = User.objects.filter(Email = email).values()
    if bool(data):
        if data.count() > 1:
            raise Exception(f"Duplicated user email [{email}]")
        if data[0]["Password"] == password:
            _active_user = data
            return True
        else:
            print("No es usted papi")
    return False

def link_user_session(email:str, key:str):
    now = datetime.now()
    session_obj = Session (
        session_key = key,
        user_email = email,
        creation_date = now,
        expire_date = datetime(
            now.year + 1,
            now.month,
            now.day,
            now.hour,
            now.minute,
            now.second,
            now.microsecond
        )
    )
    session_obj.save()

def id_generator(size=50, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



