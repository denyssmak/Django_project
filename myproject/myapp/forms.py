from django import forms
from .models import Questionnaires, Comment, MyUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
	class Meta:
		model = MyUser
		fields = ('username', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
	class Meta:
		model = MyUser
		fields = ('username', 'password')

class QuestionnairesCreateForm(forms.ModelForm):
	class Meta:
		model = Questionnaires
		fields = ('importance', 'title', 'text', 'status')


class QuestionnairesUpdateForm(forms.ModelForm):
	class Meta:
		model = Questionnaires
		fields = ('importance', 'title', 'text', 'status')


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('text',)


class AceptQuestionnairesForm(forms.ModelForm):
	consideration = forms.HiddenInput()
	class Meta:
		model = Questionnaires
		fields = ('consideration',)


class RejectQuestionnairesForm(forms.ModelForm):
	class Meta:
		model = Questionnaires
		fields = '__all__'


class RepairQuestionnairesForm(forms.ModelForm):
	class Meta:
		model = Questionnaires
		fields = ('repair',)