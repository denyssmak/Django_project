from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, View
from .models import Questionnaires, Comment
from django.contrib.auth import authenticate, login
from .forms import QuestionnairesCreateForm, RejectQuestionnairesForm, QuestionnairesUpdateForm, CommentForm, AceptQuestionnairesForm, RepairQuestionnairesForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin


class TestUserPermissionUpdate(UserPassesTestMixin):                         
    def test_func(self):                                                       
        return self.request.user == self.get_object().user


class QuestionnairesView(ListView):
    model = Questionnaires
    template_name = 'index.html'
    def get_queryset(self):
        if self.request.user.is_authenticated:
            if not self.request.user.is_superuser:
                return Questionnaires.objects.filter(user=self.request.user)
            return Questionnaires.objects.all().filter(status=True)



class QuestionnairesListView(ListView):
    model = Questionnaires
    template_name = 'questionnaires_list.html'



class QuestionnairesCreateView(CreateView):
    model = Questionnaires
    form_class = QuestionnairesCreateForm
    template_name = 'questionnaires_create.html'
    success_url = reverse_lazy('index')
    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        return super().form_valid(form=form)


class QuestionnairesUpdateVirw(TestUserPermissionUpdate, UpdateView):
    model = Questionnaires
    template_name = 'questionnaires_update.html'
    success_url = reverse_lazy('index')
    form_class = QuestionnairesUpdateForm


class RegisterUserView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('index')


class MyloginView(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('index')
    def get_success_url(self):
        return self.success_url


class MyUserlogoutView(LogoutView):
    next_page = reverse_lazy('index')


class CommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        questionnaires = Questionnaires.objects.get(id=self.kwargs['pk'])
        if questionnaires.status is False:
            raise ValueError('403')  
        object.questionnaires = questionnaires
        object.save()
        return super().form_valid(form=form)
            


class AceptQuestionnairesView(UpdateView):
    model = Questionnaires
    success_url = reverse_lazy('index')
    template_name = 'acept_questionnaires.html'
    form_class = AceptQuestionnairesForm

    def form_valid(self, form):
        if self.get_object().consideration:
            messages.error(self.request, 'Заявку приняли!')
            return redirect('/')
        elif self.get_object().consideration is False:
            messages.error(self.request, 'Заявку отклонили!')
            return redirect('/')
        else:
            object = form.save(commit=False)
            object.consideration = True
        return super().form_valid(form=form)


class RejectQuestionnairesView(CreateView):
    model = Comment
    success_url = reverse_lazy('index')
    template_name = 'reject_questionnaires.html'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        questionnaires = Questionnaires.objects.get(id=pk)
        if questionnaires.consideration:
            messages.error(request, 'Заявку приняли!')
            return redirect('/')
        elif questionnaires.consideration is False:
            messages.error(request, 'Заявку отклонили!')
            return redirect('/')
        return super().post(request, *args, **kwargs)


    def form_valid(self, form):
        pk = self.kwargs['pk']
        questionnaires = Questionnaires.objects.get(id=pk)
        object = form.save(commit=False)
        object.questionnaires = questionnaires
        object.user = self.request.user
        questionnaires.consideration = False
        questionnaires.save()
        return super().form_valid(form=form)

class RepairQuestionnairesView(UpdateView):
    model = Questionnaires
    success_url = reverse_lazy('index')
    template_name = 'repair_questionnaires.html'
    form_class = RepairQuestionnairesForm

    def form_valid(self, form):
        pk = self.kwargs['pk']
        questionnaires = Questionnaires.objects.get(id=pk)
        object = form.save(commit=False)
        object.questionnaires = questionnaires
        object.user = self.request.user
        questionnaires.repair = True
        questionnaires.save()
        return super().form_valid(form=form)


class AdminRepairQuestionnairesView(PermissionRequiredMixin, ListView):
    permission_required = 'is_superuser'
    model = Questionnaires
    template_name = 'admin_repair_questionnaires.html'
    context_object_name = 'questionnaires'


class AdminAceptRepairQuestionnairesView(UpdateView):
    model = Questionnaires
    success_url = reverse_lazy('index')
    template_name = 'admin_acept_repair_questionnaires.html'
    form_class = AceptQuestionnairesForm
    def form_valid(self, form):
        pk = self.kwargs['pk']
        questionnaires = Questionnaires.objects.get(id=pk)
        object = form.save(commit=False)
        object.questionnaires = questionnaires
        object.user = self.request.user
        questionnaires.consideration = True
        questionnaires.save()
        return super().form_valid(form=form)

class AdminRejectRepairQuestionnairesView(PermissionRequiredMixin, DeleteView):
    permission_required = 'is_superuser'
    model = Questionnaires
    success_url = reverse_lazy('index')
    template_name = 'admin_reject_repair_questionnaires.html'
    