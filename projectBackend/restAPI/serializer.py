from rest_framework import serializers # type: ignore
from .models import UserLogin, studentRecord

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLogin
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class studentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = studentRecord
        fields = '__all__'

