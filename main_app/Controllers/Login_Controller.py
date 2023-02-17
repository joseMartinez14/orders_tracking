import json

from django.views import View
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.db import connections
from django.db import connection
from django.template import loader
from main_app.config import get_server_host
import os

from main_app.models import User


class Login_Controller(View):

    def get(self, request):
        #I guess I need to check cache and to see if is logged in or session?
        template = loader.get_template('Login.html')
        data = prepare_login_data()
        return HttpResponse(template.render(data, request))
    
    def post(self, request):
        print("Got to post on Test_Controller")
        request.session['algo_estupido'] = "puta vida"

        x = json.loads(request.body)
        print(x)

        print("------------")
        session = request.session.session_key

        print(session)

        galletas = request.COOKIES
        print("Galletas:")
        print(galletas)

        print("------ call make_login -------")
        db_user = make_login(x["usuario"], x["contrasenna"])
        print (db_user)

        #No se como hacer lo de la session
        print("------ generate key ---------")
        random_key = os.urandom(16)
        print(random_key)


        template = loader.get_template('Login.html')
        return HttpResponse(template.render({}, request))
    
    def put(self, request):
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
            return data[0]
        else:
            print("No es usted papi")
    return None
    


