from django import forms
from .models import Questionnaires, Comment
from django.contrib.auth.forms import AuthenticationForm

# class QuestionnairesCreateForm(forms.ModelForm):
# 	class Meta:
# 		model = Questionnaires
# 		fields = ('importance', 'title', 'text', 'status')
# 	def save(self, commit=True):
# 		questionnaires = super().save(commit=False)
# 		if commit:
# 			questionnaires.save()
# 		return questionnaires 


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
		models = Comment
		fields = '__all__'


class AceptQuestionnairesForm(forms.ModelForm):
	class Meta:
		model = Questionnaires
		fields = '__all__'