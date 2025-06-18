from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics
from rest_framework.response import Response
from books.models import Book
from users.models import User
from rest_framework.views import APIView

from .serializers import BookSerializer, UserSerializer
from .utils.authentication import CustomJWTAuthentication
from .utils.token import (decode_access_token,
                          generate_access_token,
                          generate_refresh_token)
import json
from django.http import JsonResponse


# Create your views here.
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        auth_header = self.request.headers.get('Authorization', '')

        if not auth_header.startswith('Bearer '):
            raise Exception('Authorization header missing or invalid')

        token = auth_header.split(' ')[1]
        payload = decode_access_token(token)
        user = User.objects.get(username=payload['username'])

        serializer.save(user=user)

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(username=username)
            if user.password == password:
                access_token = generate_access_token(username)
                refresh_token = generate_refresh_token(username)
            else:
                raise Exception('Invalid password')
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=400)
        return JsonResponse({'access_token': access_token, 'refresh_token': refresh_token}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



