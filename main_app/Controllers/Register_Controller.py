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
from django.contrib.auth.models import User as auth_user
from django.contrib.auth.hashers import make_password

from main_app.models import User, Session



class Register_Controller(APIView):

    def get(self, request):
        #I guess I need to check cache and to see if is logged in or session?
        template = loader.get_template('Registration.html')
        data = prepare_data()
        return HttpResponse(template.render(data, request))
    
    def post(self, request):
        pass

    def put(self, request):
        x = json.loads(request.body)

        result = register_user(x)
        try:
            if(result == "username_existis"):
                return Response({"message":"Username already exists"}, status=status.HTTP_302_FOUND)
            elif(result == "success"):
                return Response({}, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request):
        pass

def register_user(data):

    if ( auth_user.objects.filter(username = data["username"]).exists()
        or 
        auth_user.objects.filter(email = data["email"]).exists()):
        return "username_existis"

    new_user = auth_user.objects.create_user(data["username"])
    hash_password = make_password(data["password"])
    new_user.password = hash_password
    new_user.email = data["email"]
    new_user.first_name = data["name"]
    new_user.last_name = data["lastname"]
    new_user.save()

    user = User(
            Email= data["email"],
            Username= data["username"] ,
            Password= "Se va a quitar" ,
            Name= data["name"],
            Birthdate= data["birthdate"]
            )
    user.save()
    return "success"    

def prepare_data():
    host = get_server_host()
    return {
        "server" : host
    }


