from django.db import models
from django.contrib.auth.models import User

IMPORTANCE_CHOICE = (('low','low'),
				('middle','middle'),
				('high','high'))


class Questionnaires(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	importance = models.CharField(choices=IMPORTANCE_CHOICE, max_length=10)
	title = models.CharField(max_length=100)
	text = models.TextField()
	status = models.BooleanField(default=True)

	def __str__(self):
		return f'{self.user} | {self.importance} | {self.title} | status: {self.status}'

class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField()