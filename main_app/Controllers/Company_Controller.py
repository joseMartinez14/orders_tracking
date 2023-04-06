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


from main_app.models import Company, Mapping_Usuario_Empresa


class Company_Controller(APIView):

    def get(self, request):
        #I guess I need to check cache and to see if is logged in or session?
        template = loader.get_template('Create_Company.html')
        session = request.COOKIES.get("sessionid","")
        data = prepare_data(session)
        if (data is None):
             return redirect('main_app:Login')
        return HttpResponse(template.render(data, request))
    
    def post(self, request):
        pass

    def put(self, request):
        print("Got to post on Company_Controller put")
        session = request.COOKIES.get("sessionid","")
        x = json.loads(request.body)
        print("This is the body")
        print(x)

        print("This is the data")
        print(request.data)

        try:
            result = create_company(x, session)
            if(result == 'UNAVAILABLE'):
                return Response({}, status=status.HTTP_302_FOUND)
            return Response({}, status=status.HTTP_200_OK)
        except:
            print("An exception occurred") 
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request):
        pass


def create_company(json_data, session):
    if(session == "" or session is None):
        #Return none. So controller can redirect
        return None
    
    if(get_company_by_session(session)):
        return "UNAVAILABLE"
    
    _user = get_user_by_session(session)


    company = Company(
        Name = json_data["company_name"],
        Description = json_data["company_description"],
        membership = True,
        Creation_date = datetime.now(),
        Last_membership_update = datetime.now()
    )
    company.save()

    mapping = Mapping_Usuario_Empresa(User_id = _user, Company= company, Level= "Owner")

    mapping.save()




def prepare_data(session):
    if(session == "" or session is None):
        #Return none. So controller can redirect
        return None
    
    _user = get_user_by_session(session)

    host = get_server_host()
    return {
        "server" : host,
        "current_user" : _user
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
    print("aqui aquiu aqui")
    print(session)
    s = Session.objects.get(pk=session)
    user_logged_in = s.get_decoded()
    _user_id = user_logged_in["_auth_user_id"]
    try:
        mapping = Mapping_Usuario_Empresa.objects.filter(User_id = _user_id ).get()
        return True
    except:
        return False