from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import make_password

# Create your models here.

class User(models.Model):
    Email = models.CharField(max_length=40, null=False, unique=True)
    Username = models.CharField(max_length=40, null=False)
    Password = models.CharField(max_length=200, null=False)
    Name = models.CharField(max_length=40, null=False)
    Birthdate = models.DateField()
    User_Since = models.DateField(auto_now=True)
    
    def save(self, *args, **kwargs):
        self.Password = make_password(self.Password)
        super(User, self).save(*args, **kwargs)


class Session(models.Model):
    session_key = models.CharField(max_length=60, primary_key = True)
    user_email = models.CharField(max_length=40, null=False)
    creation_date = models.DateTimeField(auto_now=False, null=False)
    expire_date = models.DateTimeField(auto_now=False, null=False)

class Company(models.Model):
    Name = models.CharField(max_length=45, null=False)
    Description = models.CharField(max_length=250, null=False)
    membership = models.BooleanField(default=False)
    #Logo = models.ImageField(null=True)  ????
    Creation_date = models.DateTimeField(auto_now=False, null=False)
    Last_membership_update = models.DateTimeField(auto_now=False, null=False)
    #ID implicito

class Mapping_Usuario_Empresa(models.Model):
    #ID implicito
    User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Company = models.ForeignKey(Company, on_delete=models.CASCADE)
    Level = models.CharField(max_length=10, null=False) #Esto podria ser una normmalized table. Owner, Admin or member

class Company_Process(models.Model):
    #ID Implicito
    Process_Name = models.CharField(max_length=20, null=False)
    Description = models.CharField(max_length=150, null=False)
    Company = models.ForeignKey(Company, on_delete=models.CASCADE)

class Company_Process_step_template(models.Model):
    #ID Implicito
    Step_Name = models.CharField(max_length=20, null=False)
    Step_Order_Number = models.IntegerField(null=False) #Este es el orden en que va el step si es el primero o ultimo
    Description = models.CharField(max_length=150, null=False)
    Company_Process = models.ForeignKey(Company_Process, on_delete=models.CASCADE)
    
class Company_Client(models.Model):
    #ID Implicito
    Name = models.CharField(max_length=50, null=False)
    Cellphone = models.CharField(max_length=25, null=False)
    Email = models.CharField(max_length=70, null=False)
    Address = models.CharField(max_length=200, null=False)
    Company = models.ForeignKey(Company, on_delete=models.CASCADE)

class Company_Order(models.Model):
    #ID Implicito
    Company = models.ForeignKey(Company, on_delete=models.CASCADE)
    Client = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    Date_Received = models.DateTimeField(auto_now=False, null=False)
    Description = models.CharField(max_length=500, null=False)
    Status = models.CharField(max_length=10, null=False)

class Process_Step_Client(models.Model):
    #ID Implicito
    Company_Process_step_template = models.ForeignKey(Company_Process_step_template, on_delete=models.CASCADE)
    Order = models.ForeignKey(Company_Order, on_delete=models.CASCADE)
    Notes = models.CharField(max_length=100, null=True)
    Status = models.CharField(max_length=10, null=False)





