import secrets

from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView

from config import settings
from users.forms import UserRegisterForm, UserForm
from users.models import User


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserCreateView(CreateView):
    model = User
    template_name = 'register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('mailings:home')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/email-confirm/{token}/'
        send_mail(
            'Подтверждение почты',
            f'Добро пожаловать на сервис для рассылок! Для подтверждения регистрации перейдите по ссылке: {url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )
        return super().form_valid(form)


class PasswordResetUserView(PasswordResetView):
    template_name = 'reset_password.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    from_email = settings.DEFAULT_FROM_EMAIL
    success_url = reverse_lazy('users:password_reset_done')


class UserDetailView(DetailView):
    template_name = 'user_detail.html'
    model = User


class UserUpdateView(UpdateView):
    template_name = 'user_form.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('mailings:home')

    def get_success_url(self):
        return reverse('users:user_detail', args=[self.kwargs.get('pk')])
