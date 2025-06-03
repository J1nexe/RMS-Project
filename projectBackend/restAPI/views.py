from rest_framework import generics, status # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.views import APIView # type: ignore
from .models import UserLogin, studentRecord
from .serializer import UserSerializer, studentRecordSerializer, LoginSerializer

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

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                user = UserLogin.objects.get(email=email)
                if user.password == password:  # Note: In a production environment, you should use proper password hashing
                    user_data = UserSerializer(user).data
                    return Response({
                        'message': 'Login successful',
                        'user': user_data,
                        'status': 'success'
                    })
                else:
                    return Response({
                        'error': 'Invalid credentials'
                    }, status=status.HTTP_401_UNAUTHORIZED)
            except UserLogin.DoesNotExist:
                return Response({
                    'error': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
