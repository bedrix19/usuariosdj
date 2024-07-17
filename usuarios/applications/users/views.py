from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import View, CreateView
from django.views.generic.edit import FormView

from .models import User
from .functions import code_generator
from .forms import (
    UserRegisterForm,
    LoginForm,
    PasswordUpdateForm,
    VerificationForm,
)

# Create your views here.

# esta vista no es buena para registrar usuario con contraseña
# class UserRegisterView(CreateView):
#     template_name = "users/register.html"
#     form_class = UserRegisterForm
#     success_url = '/'

class UserRegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        #generamos el codigo
        codigo = code_generator()
        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero'],
            codregistro=codigo,
        )
        ## Deberia funcionar con esto pero no wa darle permisos
        ## # enviar email
        ## send_mail(
        ##     'Confirmación de email',
        ##     'Codigo de verificación:\t'+codigo,
        ##     'Xemail-practicasD@gmail.com',
        ##     [form.cleaned_data['email']],
        ## )
        ## # redirigir a pantalla de validación
        return HttpResponseRedirect(
            reverse(
                'users_app:user-verificar',
                kwargs={'pk':usuario.id},
            )
        )
        #return super().form_valid(form)

class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:home-panel')

    def form_valid(self, form):
        user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password'],
        )
        login(self.request, user)
        return super().form_valid(form)
    
class LogoutView(View):

    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )

class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'users/update.html'
    form_class = PasswordUpdateForm
    success_url = reverse_lazy('users_app:user-login')
    login_url = reverse_lazy('users_app:user-login') # necesario para LoginRequiredMixin

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            username = usuario.username,
            password = form.cleaned_data['password1'],
        )

        if user :
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()

        logout(self.request)
        return super().form_valid(form)
    
class CodeVerification(FormView):
    template_name = 'users/verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:user-login')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'pk':self.kwargs['pk'],
        })
        return kwargs

    def form_valid(self, form):
        #
        User.objects.filter(id=self.kwargs['pk']).update(is_active=True)
        return super().form_valid(form)
