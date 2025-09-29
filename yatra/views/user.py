from functools import partial
from rest_framework.generics import ListAPIView
from core.utils import SearchPagination
from yatra.filters import UserFilter
from yatra.serializers.user import UserSerializer, CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework.permissions import DjangoModelPermissions
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response

User = get_user_model()

class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class Refresh(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

class RegisterView(APIView):
    permission_classes = [DjangoModelPermissions]
    queryset = User.objects.none()

    def post(self, request):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        d1 = UserSerializer(user, fields=['id', 'created_on', 'name', 'number', 'is_active']).data
        d2 = {'success_message': ['User registered successfully.']}
        d2.update(d1)
        return Response(d2)

class UserList(ListAPIView):
    serializer_class = partial(UserSerializer, exclude=['is_superuser', 'groups', 'user_permissions'])
    permission_classes = [DjangoModelPermissions]
    queryset = User.objects.all()
    pagination_class = SearchPagination
    filterset_class = UserFilter
    filterset_fields = UserFilter.Meta.fields
    search_fields = UserFilter.fizzy_fields