
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','Email', 'Password','Name', 'Birthdate', 'User_Since']

