
from re import template
from urllib import request
from django.shortcuts import redirect

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, UpdateView , DeleteView , FormView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login
 
from django.contrib.auth.views  import LoginView


from . models import *








class RegisterUser(FormView):
    redirect_authenticated_user= True
    form_class = UserCreationForm
    template_name= 'register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form) :
        user= form.save()
        if user is not None:
            login(self.request , user)
        return super(RegisterUser, self).form_valid(form)

    def get(self, *k , **kwarg):
            if self.request.user.is_authenticated:
                return redirect('home')
            return super(RegisterUser, self).get(*k , **kwarg)



class CustomLogin(LoginView):
    fields = '__all__'
    redirect_authenticated_user= True
    template_name= 'login.html'

    def get_success_url(self) -> str:
        return reverse_lazy('home')






class TaskList(LoginRequiredMixin ,ListView):
    model= Task
    template_name= 'home.html'
    context_object_name= 'tasks'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tasks']= context['tasks'].filter(user=self.request.user)
        context['count']= context['tasks'].filter(is_completed=False).count

        search_input= self.request.GET.get('search-area') or ''
        if  search_input:
            context['tasks']= context['tasks'].filter(title__icontains= search_input)
           

        return context



class TaskDetail(LoginRequiredMixin,DetailView):
    model= Task
    template_name= 'detail.html'
    context_object_name= 'item'


class CreateTask(LoginRequiredMixin,CreateView):
    model= Task
    fields= ['title','description','is_completed']
    template_name= 'create.html'
    # context_object_name= 'tasks'
    success_url= reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user= self.request.user
        return super(CreateTask, self).form_valid(form)
        


class UpdateTask(LoginRequiredMixin,UpdateView):
    model= Task
    fields= ['title','description','is_completed']

    template_name= 'update.html'
    success_url= reverse_lazy('home')
    context_object_name= 'task'

    def form_valid(self, form):
        form.instance.user= self.request.user
        return super(UpdateTask, self).form_valid(form)

class DeleteTask(LoginRequiredMixin,DeleteView):
    model= Task
    # fields= '__all__'
    template_name= 'delete.html'
    success_url= reverse_lazy('home')
    context_object_name= 'task'
