from myapp.models import Questionnaires, Comment
from django.contrib.auth.models import User
from myapp.api.serializers import RegisterUserSerializer, QuestionnairesSerializer                            
from rest_framework.response import Response
from rest_framework import viewsets


class RegisterUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    http_method_names = ['get', 'post', 'put', 'patch']


class QuestionnairesViewSet(viewsets.ModelViewSet):
    queryset = Questionnaires.objects.all()
    serializer_class = QuestionnairesSerializer
    http_method_names = ['get', 'post', 'put', 'patch']
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)