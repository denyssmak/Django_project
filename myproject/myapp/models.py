from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.utils import timezone

IMPORTANCE_CHOICE = (('low','low'),
				('middle','middle'),
				('high','high'))

class Questionnaires(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	importance = models.CharField(choices=IMPORTANCE_CHOICE, max_length=10)
	title = models.CharField(max_length=100)
	text = models.TextField()
	status = models.BooleanField(default=True)
	consideration = models.BooleanField(null=True, blank=True)
	repair = models.BooleanField(null=True, blank=True)


	def __str__(self):
		return f'{self.user} | {self.importance} | {self.title} | status: {self.status} |consideration: {self.consideration} |repair: {self.repair}'

class Comment(models.Model):
	questionnaires = models.ForeignKey(Questionnaires, on_delete=models.CASCADE, related_name='comment_questionnaires')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
	text = models.TextField()
	def __str__(self):
		return f'{self.user} | {self.text}'

class MyToken(Token):
    time_to_die = models.DateTimeField(default=timezone.now)