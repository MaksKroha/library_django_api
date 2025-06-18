from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import BookViewSet, UserCreateView, login

router_book = DefaultRouter()
router_book.register(r'books', BookViewSet)

router_user = DefaultRouter()
router_user.register(r'users', UserCreateView)

urlpatterns = [
    path('api/', include(router_book.urls) ),
    path('api/users/create', UserCreateView.as_view(), name='user-create' ),
    path('api/users/login', login, name='user-login' ),
]