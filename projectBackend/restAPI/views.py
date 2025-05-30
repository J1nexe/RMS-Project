from rest_framework import generics # type: ignore
from .models import UserLogin, studentRecord
from .serializer import UserSerializer, studentRecordSerializer

class UserList(generics.ListCreateAPIView):
    queryset = UserLogin.objects.all()
    serializer_class = UserSerializer

class studentRecordList(generics.ListCreateAPIView):
    queryset = studentRecord.objects.all()
    serializer_class = studentRecordSerializer
