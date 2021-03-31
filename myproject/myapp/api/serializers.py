from django.urls import path, include
from django.contrib.auth.models import User
from myapp.models import Questionnaires, Comment
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2')

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Пароль не совподает')
        return data

class QuestionnairesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaires
        fields = ('id', 'importance', 'title', 'text', 'status',)
        read_only = ('id')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'questionnaires')
        read_only = ('id')


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text',)
        read_only = ('id')


class QuestionnairesListSerializer(serializers.ModelSerializer):
    comment_questionnaires = CommentsSerializer(read_only=True, many=True)
    class Meta:
        model = Questionnaires
        fields = ('id', 'importance', 'title', 'text', 'status', 'comment_questionnaires')
        read_only = ('id')