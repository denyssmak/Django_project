from django.test import TestCase
from django.urls import reverse
from myapp.models import MyUser, Questionnaires, Comment
from myapp.forms import QuestionnairesCreateForm, CustomUserCreationForm, CustomAuthenticationForm, RejectQuestionnairesForm, QuestionnairesUpdateForm, CommentForm, AceptQuestionnairesForm, RepairQuestionnairesForm
from django.utils import timezone


class QuestionnairesCreateFormTest(TestCase):
    
    def setUp(self):
        self.user = MyUser.objects.create_user(username='Testic', password='qwe123ewq')    

    def test_create_questionnaires(self):
        form_data = {user:self.user'importance':'low', 'title':'title',
                     'text':'text', 'status':True}
        form = QuestionnairesCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

class QuestionnairesUpdateFormTest(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create_user(username='Testic', password='qwe123ewq')
        self.q1 = Questionnaires.objects.create(importance='low', title='title', text="t", status= True)

    def test_update_questionnaires(self):
        form_data = {'importance':'high', 'title':'title',
                     'text':'text', 'status':True}
        form = QuestionnairesCreateForm(instance=self.q1, data=form_data)
        self.assertFalse(form.is_valid())
