from myapp.models import Questionnaires, Comment
from django.contrib.auth.models import User
from myapp.api.serializers import RegisterUserSerializer, QuestionnairesSerializer, CommentSerializer                          
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class RegisterUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    http_method_names = ['get', 'post', 'put', 'patch']


class QuestionnairesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Questionnaires.objects.all()
    serializer_class = QuestionnairesSerializer
    http_method_names = ['get', 'post', 'put', 'patch']
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post']
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
         