import datetime

from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

def home(request):
    return render(request, 'home/home.html')

class HomePage(LoginRequiredMixin, TemplateView):
    template_name = "home/index.html"
    login_url = reverse_lazy('users_app:user-login') # necesario para LoginRequiredMixin

class FechaMixin(object):

    def get_context_data(self, **kwargs):
        context = super(FechaMixin, self).get_context_data(**kwargs)
        context['fecha'] = datetime.datetime.now()
        return context

class TemplatePruebaMixin(FechaMixin, TemplateView):
    template_name = "home/mixin.html"
