from myapp.models import Questionnaires, Comment, MyToken
from django.contrib.auth.models import User
from myapp.api.serializers import RegisterUserSerializer, QuestionnairesSerializer, CommentSerializer, QuestionnairesListSerializer                         
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from django.utils import timezone
from datetime import timedelta
from myapp.api.permissions import CommentPermisson, QuestionnairesUpdatePermisson
from rest_framework.authtoken.views import ObtainAuthToken

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
    permission_classes = [IsAuthenticated, QuestionnairesUpdatePermisson]
    queryset = Questionnaires.objects.all()
    serializer_class = QuestionnairesSerializer
    http_method_names = ['get', 'post', 'put', 'patch']
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, CommentPermisson]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post']
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class QuestionnairesListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Questionnaires.objects.all()
    serializer_class = QuestionnairesListSerializer


