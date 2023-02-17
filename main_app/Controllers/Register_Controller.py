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

from main_app.models import User


class Register_Controller(APIView):

    def get(self, request):
        #I guess I need to check cache and to see if is logged in or session?
        template = loader.get_template('Registration.html')
        data = prepare_data()
        return HttpResponse(template.render(data, request))
    
    def post(self, request):
        pass

    def put(self, request):
        print("Got to post on Register_Controller put")

        x = json.loads(request.body)

        if (register_user(x) is True):
            print("Tiene que ser successfully ")
            return Response({}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request):
        pass

def register_user(data):

    print(data)

    existing_user = User.objects.filter(Email = data["email"]).values()
    print("Que encontro?")
    print(existing_user)
    if bool(existing_user):
        return False
    print("Vamos a guardar la mierda")
    user = User(
            Email= data["email"],
            Username= data["username"] ,
            Password= data["password"] ,
            Name= data["name"],
            Birthdate= data["birthdate"]
            )
    user.save()
    return True

def prepare_data():
    host = get_server_host()
    return {
        "server" : host
    }