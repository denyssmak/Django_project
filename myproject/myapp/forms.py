from django import forms
from .models import Questionnaires, Comment
from django.contrib.auth.forms import AuthenticationForm


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