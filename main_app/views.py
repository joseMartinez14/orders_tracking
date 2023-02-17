from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def members(request):
    template = loader.get_template('Example.html')
    return HttpResponse(template.render())


    
def registration_example(request):
    template = loader.get_template('Registration_Example.html')
    return HttpResponse(template.render())

def login_example(request):
    template = loader.get_template('Login_Example.html')
    return HttpResponse(template.render())