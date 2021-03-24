from django.urls import include, path
from .views import QuestionnairesCreateView, AceptQuestionnairesView, RejectQuestionnairesView, CommentView, QuestionnairesView, RegisterUserView, MyloginView, MyUserlogoutView, QuestionnairesListView, QuestionnairesUpdateVirw, RepairQuestionnairesView, AdminRepairQuestionnairesView, AdminAceptRepairQuestionnairesView, AdminRejectRepairQuestionnairesView

	
urlpatterns = [
	path('', QuestionnairesView.as_view(), name='index'),
	path('login/', MyloginView.as_view(), name='login_page'),
    path('register/', RegisterUserView.as_view(), name='register_page'),
    path('logout/', MyUserlogoutView.as_view(), name='logout_page'),
	path('questionnaires_create/', QuestionnairesCreateView.as_view(), name='questionnaires_create'),
    path('questionnaires_update/<int:pk>/', QuestionnairesUpdateVirw.as_view(), name='questionnaires_update'),
    path('questionnaires_list/', QuestionnairesListView.as_view(), name='questionnaires_list'),
    path('comments/<int:pk>/', CommentView.as_view(), name='comments'),
    path('acept_questionnaires/<int:pk>/', AceptQuestionnairesView.as_view(), name='acept_questionnaires'),
	path('reject_questionnaires/<int:pk>/', RejectQuestionnairesView.as_view(), name='reject_questionnaires'),
	path('repair_questionnaires/<int:pk>/', RepairQuestionnairesView.as_view(), name='repair_questionnaires'),
	path('admin_repair_questionnaires/', AdminRepairQuestionnairesView.as_view(), name='admin_repair_questionnaires'),
	path('admin_acept_repair_questionnaires/<int:pk>/', AdminAceptRepairQuestionnairesView.as_view(), name='admin_acept_repair_questionnaires'),
	path('admin_reject_repair_questionnaires/<int:pk>/', AdminRejectRepairQuestionnairesView.as_view(), name='admin_reject_repair_questionnaires'),
]