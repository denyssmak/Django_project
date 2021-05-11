from django.test import TestCase
from django.urls import reverse
from myapp.models import MyUser, Questionnaires, Comment
from myapp.forms import QuestionnairesCreateForm, CustomUserCreationForm, CustomAuthenticationForm, RejectQuestionnairesForm, QuestionnairesUpdateForm, CommentForm, AceptQuestionnairesForm, RepairQuestionnairesForm
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from unittest import skip
from django.contrib.messages import get_messages

class UserLoginViewTest(TestCase):

    def setUp(self):
        self.data = {'username': 'admin', 'password': '123'}
        self.user = MyUser.objects.create_user(**self.data)
        self.url = reverse('login_page')

    def test_user_login_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.failUnless(isinstance(response.context['form'], AuthenticationForm))

    def test_user_login_post_succes(self):
        response = self.client.post(self.url, data=self.data, follow=True)
        session = self.client.session['time_action']
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTrue(session, timezone.now())

    def test_user_login_post_succes_redirect(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))

    def test_user_login_post(self):
        data = {'username': 'admin', 'password': 'a'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())


class UserRegisterViewTest(TestCase):

    def setUp(self):
        self.url = reverse('register_page')
        self.data = {'username': 'admin', 'password1': '123', 'password2': '123'}

    def test_user_register_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        

    def test_user_register_post_succes(self):
        response = self.client.post(self.url, data=self.data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(MyUser.objects.count(), 1)

    def test_user_register_post_redirect(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))

    def test_user_register_post_failure(self):
        data = {'username': 'admin', 'password1': '1df2q', 'password2': 'offfw3'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(MyUser.objects.count(), 0)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue(response.context['form'].errors)


class UserLogoutView(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create_user(username='admin', password='123')
        self.client.force_login(self.user)
        self.url = reverse('logout_page')

    def test_user_logout_get(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_user_logout_get_redirect(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))

class QuestionnairesViewTest(TestCase):

    def setUp(self):
        self.url = reverse('index')
        self.user = MyUser.objects.create_user(username='Testic', password='qwe123ewq')
        self.user2 = MyUser.objects.create_user(username='mm', password='1')  
        self.client.force_login(user=self.user)
        self.q1 = Questionnaires.objects.create(user=self.user, importance='middle',
                                                title='title', text='text', status=True,
        )
        self.q2 = Questionnaires.objects.create(user=self.user, importance='low',
                                                title='title', text='text', status=True,
        )
        self.q3 = Questionnaires.objects.create(user=self.user2, importance='low',
                                                title='title', text='text', status=True,
        )

    def test_url(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_questionnaires_user(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['questionnaires_list'].count(),
            Questionnaires.objects.filter(user=self.user2).count()
        )

    def test_questionnaires_super_user(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['questionnaires_list'].count(), 
                         Questionnaires.objects.count()
        )

class QuestionnairesCreateViewTest(TestCase):

    def setUp(self):
        #breakpoint()
        self.url = reverse('questionnaires_create')
        self.user = MyUser.objects.create_user(username='Testic', password='qwe123ewq')
        self.user2 = MyUser.objects.create_user(username='mm', password='1')  
        self.q1 = Questionnaires.objects.create(user=self.user, importance='middle',
                                                title='title', text='text', status=True,
        )
        self.q2 = Questionnaires.objects.create(user=self.user, importance='low',
                                                title='title', text='text', status=True,
        )
        self.q3 = Questionnaires.objects.create(user=self.user2, importance='low',
                                                title='title', text='text', status=True,
        )

    def test_url(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questionnaires_create.html')

    def test_questionnaires_redirect(self):
        self.client.force_login(self.user)
        data = {'importance':'low','title':'title', 'text':'text'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))

    def test_questionnaires_create(self):
        self.client.force_login(self.user)
        data = {'importance':'low','title':'title', 'text':'text'}
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Questionnaires.objects.count(), 4)

    def test_questionnaires_create_no_login(self):
        data = {'importance':'low','title':'title', 'text':'text'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)

class QuestionnairesUpdateView(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create_user(username='Testic', password='qwe123ewq')
        self.user2 = MyUser.objects.create_user(username='mm', password='1')  
        self.q1 = Questionnaires.objects.create(user=self.user, importance='middle',
                                                title='title', text='text',status=True,
        )
        self.q2 = Questionnaires.objects.create(user=self.user, importance='low',
                                                title='title', text='text', status=True,
        )
        self.q3 = Questionnaires.objects.create(user=self.user2, importance='low',
                                                title='title', text='text', status=True,
        )
        self.url = reverse('questionnaires_update', kwargs={'pk': self.q1.pk})

    def test_url(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questionnaires_update.html')

    def test_update_redirect(self):
        self.client.force_login(self.user)
        data = {'importance':'low','title':'title1', 'text':'text'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))

    def test_url_another_user(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_questionnaires_update(self):
        self.client.force_login(self.user)
        data = {'importance':'middle','title':'title2', 'text':'text2'}
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Questionnaires.objects.count(), 3)

    def test_questionnaires_update_no_login(self):
        data = {'importance':'low','title':'title2', 'text':'text2'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)

class CommentViewTest(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create_user(username='Testic', password='qwe123ewq')
        self.user2 = MyUser.objects.create_user(username='mm', password='1')  
        self.q1 = Questionnaires.objects.create(user=self.user, importance='middle',
                                                title='title', text='text', status=True,
        )
        self.q2 = Questionnaires.objects.create(user=self.user, importance='low',
                                                title='title', text='text', status=True,
        )
        self.q3 = Questionnaires.objects.create(user=self.user2, importance='low',
                                                title='title', text='text', status=False,
        )
        self.c1 = Comment.objects.create(user=self.user, 
                                        questionnaires=self.q1,
                                        text='bla'
        )
        # self.url = reverse('comments', kwargs={'pk': self.c1.pk})

    def test_url(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('comments', kwargs={'pk': self.q1.pk})
)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comments.html')

    def test_comment_redirect(self):
        self.client.force_login(self.user)
        data = {'text':'text'}
        response = self.client.post(reverse('comments', kwargs={'pk': self.q1.pk})
, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))

    def test_comment_create(self):
        self.client.force_login(self.user)
        data = {'text':'text'}
        response = self.client.post(reverse('comments', kwargs={'pk': self.q1.pk})
, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 2)

    def test_comment_create_no_login(self):
        data = {'text':'text'}
        response = self.client.post(reverse('comments', kwargs={'pk': self.q1.pk})
, data)
        self.assertEqual(response.status_code, 302)

    @skip
    def test_comment_create_status_false(self):
        self.client.force_login(self.user)
        data = {'text':'text'}
        response = self.client.post(reverse('comments', kwargs={'pk': self.q3.pk})
, data)
        self.assertRaises(response.status_code, ValueError)


class AceptQuestionnairesViewTest(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create_user(username='Testic', password='qwe123ewq')
        self.user2 = MyUser.objects.create_user(username='mm', password='1')  
        self.q1 = Questionnaires.objects.create(user=self.user, importance='middle',
                                                title='title', text='text', status=True,
        )
        self.q2 = Questionnaires.objects.create(user=self.user, importance='low',
                                                title='title', text='text', status=True,
                                                consideration=False,
        )
        self.q3 = Questionnaires.objects.create(user=self.user2, importance='low',
                                                title='title', text='text', status=True,
                                                consideration=True,
        )
        self.url = reverse('acept_questionnaires', kwargs={'pk': self.q1.pk})
        

    def test_url(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'acept_questionnaires.html')

    def test_acept_redirect(self):
        self.client.force_login(self.user)
        self.q1.consideration = True
        self.q1.save()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))

    def test_acept_true_questionnaires(self):
        self.client.force_login(self.user)
        url = reverse('acept_questionnaires', kwargs={'pk': self.q3.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))
        self.assertTrue(self.q3.consideration, True)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Заявку приняли!')


    def test_acept_false_questionnaires(self):
        self.client.force_login(self.user)
        url = reverse('reject_questionnaires', kwargs={'pk': self.q2.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))
        self.assertFalse(self.q2.consideration, False)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Заявку отклонили!')

class RepairQuestionnairesViewTest(TestCase):
    
    def setUp(self):
        self.user = MyUser.objects.create_user(username='Testic', password='qwe123ewq')
        self.user2 = MyUser.objects.create_user(username='mm', password='1')  
        self.q1 = Questionnaires.objects.create(user=self.user, importance='middle',
                                                title='title', text='text', status=True,
        )
        self.q2 = Questionnaires.objects.create(user=self.user, importance='low',
                                                title='title', text='text', status=True,
                                                consideration=False,
        )
        self.q3 = Questionnaires.objects.create(user=self.user2, importance='low',
                                                title='title', text='text', status=True,
                                                consideration=True,
        )
        self.url = reverse('reject_questionnaires', kwargs={'pk': self.q1.pk})

    def test_url(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reject_questionnaires.html')

    def test_reject_redirect(self):
        self.client.force_login(self.user)
        self.q1.consideration = False
        self.q1.save()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))

    def test_reject_true_questionnaires(self):
        self.client.force_login(self.user)
        url = reverse('acept_questionnaires', kwargs={'pk': self.q3.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))
        self.assertTrue(self.q3.consideration, True)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Заявку приняли!')


    def test_reject_false_questionnaires(self):
        self.client.force_login(self.user)
        url = reverse('reject_questionnaires', kwargs={'pk': self.q2.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))
        self.assertFalse(self.q2.consideration, False)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Заявку отклонили!')

class RepairQuestionnairesViewTest(TestCase):
    
    def setUp(self):
        self.user = MyUser.objects.create_user(username='Testic', password='qwe123ewq')
        self.user2 = MyUser.objects.create_user(username='mm', password='1')  
        self.q1 = Questionnaires.objects.create(user=self.user, importance='middle',
                                                title='title', text='text', status=True,
        )
        self.q2 = Questionnaires.objects.create(user=self.user, importance='low',
                                                title='title', text='text', status=True,
                                                consideration=False,
        )
        self.q3 = Questionnaires.objects.create(user=self.user2, importance='low',
                                                title='title', text='text', status=True,
                                                consideration=True,
        )
        self.url = reverse('repair_questionnaires', kwargs={'pk': self.q1.pk})

    def test_url(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'repair_questionnaires.html')

    def test_repair_redirect(self):
        self.client.force_login(self.user)
        self.q2.consideration = True
        self.q2.save()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))

    def test_repair_create(self):
        self.client.force_login(self.user)
        self.q2.consideration = True
        self.q2.save()
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 200)

class AdminRepairQuestionnairesViewTest(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create_user(username='Testic', password='qwe123ewq')
        self.url = reverse('admin_repair_questionnaires')

    def test_url(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_repair_questionnaires.html')

    def test_url_no_admin(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class AdminAceptRepairQuestionnairesView(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create_user(username='Testic', password='qwe123ewq')
        self.user2 = MyUser.objects.create_user(username='mm', password='1')  
        self.q1 = Questionnaires.objects.create(user=self.user, importance='middle',
                                                title='title', text='text', status=True,
        )
        self.q2 = Questionnaires.objects.create(user=self.user, importance='low',
                                                title='title', text='text', status=True,
                                                consideration=False,
        )
        self.q3 = Questionnaires.objects.create(user=self.user2, importance='low',
                                                title='title', text='text', status=True,
                                                consideration=True, repair=True,
        )
        self.url = reverse('admin_acept_repair_questionnaires', kwargs={'pk': self.q1.pk})

    def test_url(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_acept_repair_questionnaires.html')

    def test_acept_repair_create(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)
        self.q2.repair = True
        self.q2.save()
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_acept_repair_redirect(self):
        self.client.force_login(self.user)
        self.q2.consideration = True
        self.q2.save()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))

class AdminRejectRepairQuestionnairesView(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create_user(username='Testic', password='qwe123ewq')
        self.user2 = MyUser.objects.create_user(username='mm', password='1')  
        self.q1 = Questionnaires.objects.create(user=self.user, importance='middle',
                                                title='title', text='text', status=True,
        )
        self.q2 = Questionnaires.objects.create(user=self.user, importance='low',
                                                title='title', text='text', status=True,
                                                consideration=False,
        )
        self.q3 = Questionnaires.objects.create(user=self.user2, importance='low',
                                                title='title', text='text', status=True,
                                                consideration=True, repair=True,
        )
        self.url = reverse('admin_reject_repair_questionnaires', kwargs={'pk': self.q1.pk})

    def test_url(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_reject_repair_questionnaires.html')

    def test_reject_repair_create(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)
        self.q2.repair = False
        self.q2.save()
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 200)