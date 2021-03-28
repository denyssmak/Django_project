from myapp.models import Questionnaires, Comment, MyToken
from django.contrib.auth.models import User
from myapp.api.serializers import RegisterUserSerializer, QuestionnairesSerializer, CommentSerializer                          
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.utils import timezone
from datetime import timedelta
from myapp.api.permissions import CommentPermisson
from rest_framework.authtoken.views import ObtainAuthToken


class CustomTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):
        try:
            token = MyToken.objects.get(key=key)
        except MyToken.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid Token")
        if not token.user.is_superuser:
            if token.time_to_die + timedelta(minutes=5) < timezone.now():
                token.delete()
                raise exceptions.AuthenticationFailed("Invalid Token")
            else:
                token.time_to_die = timezone.now()
                token.save()
        return token.user, token


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = MyToken.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'time': token.time_to_die
        })


class RegisterUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    http_method_names = ['get', 'post', 'put', 'patch']


class QuestionnairesViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]
    queryset = Questionnaires.objects.all()
    serializer_class = QuestionnairesSerializer
    http_method_names = ['get', 'post', 'put', 'patch']
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated, CommentPermisson]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post']
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


         