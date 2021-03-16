from django.urls import include, path
from .views import QuestionnairesCreateView, AceptQuestionnairesView, CommentView, QuestionnairesView, RegisterUserView, MyloginView, MyUserlogoutView, QuestionnairesListView, QuestionnairesUpdateVirw

	
urlpatterns = [
	path('', QuestionnairesView.as_view(), name='index'),
	path('login/', MyloginView.as_view(), name='login_page'),
    path('register/', RegisterUserView.as_view(), name='register_page'),
    path('logout/', MyUserlogoutView.as_view(), name='logout_page'),
	path('questionnaires_create/', QuestionnairesCreateView.as_view(), name='questionnaires_create'),
    path('questionnaires_update/<int:pk>/', QuestionnairesUpdateVirw.as_view(), name='questionnaires_update'),
    path('questionnaires_list/', QuestionnairesListView.as_view(), name='questionnaires_list'),
    path('comments/', CommentView.as_view(), name='comments'),
    path('acept_questionnaires/', AceptQuestionnairesView.as_view(), name='acept_questionnaires'),
]