import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from config import settings
from mailings.models import MailingAttempts
from users.forms import UserRegisterForm, UserForm, ManagerForm
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


@method_decorator(cache_page(60 * 15), name='dispatch')
class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'user_detail.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object

        successful_attempts = MailingAttempts.objects.filter(
            mailing__owner=user,
            status=MailingAttempts.successfully
        ).count()

        unsuccessful_attempts = MailingAttempts.objects.filter(
            mailing__owner=user,
            status=MailingAttempts.not_successfully
        ).count()

        context['successful_attempts'] = successful_attempts
        context['unsuccessful_attempts'] = unsuccessful_attempts
        return context

    def get_object(self, queryset=None):
        self.object = self.request.user


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'user_form.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('mailings:home')

    def get_success_url(self):
        return reverse('users:user_detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        user = self.request.user
        if user == self.object:
            return UserForm
        if user.groups.filter(name='Managers').exists():
            return ManagerForm
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_self'] = user == self.object
        context['is_manager'] = user.groups.filter(name='Managers').exists()
        return context


class UsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'user_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='Managers').exists():
            return queryset
        raise PermissionDenied
