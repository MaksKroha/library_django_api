import jwt

from users.models import User
from rest_framework.authentication import BaseAuthentication
from main import settings
class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('Authorization')

        if not auth_header:
            return None

        token = auth_header.split()[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except Exception as e:
            print(e)
            return None

        try:
            user = User.objects.get(username=payload['username'])
        except Exception as e:
            print(e)
            return None

        return user, None