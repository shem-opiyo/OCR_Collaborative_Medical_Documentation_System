from rest_framework import serializers
from .models import Employee
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = ['id', 'user', 'role', 'department', 'contact_info', 'created_at']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer().create(user_data)
        employee = Employee.objects.create(user=user, **validated_data)
        return employee
