from rest_framework import generics, status # type: ignore
from rest_framework.response import Response # type: ignore
from .models import UserLogin, studentRecord
from .serializer import UserSerializer, studentRecordSerializer

class UserList(generics.ListCreateAPIView):
    queryset = UserLogin.objects.all()
    serializer_class = UserSerializer

class studentRecordList(generics.ListCreateAPIView):
    queryset = studentRecord.objects.all()
    serializer_class = studentRecordSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class studentRecordDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = studentRecord.objects.all()
    serializer_class = studentRecordSerializer

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
