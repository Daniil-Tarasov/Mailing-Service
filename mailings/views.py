from django.core.cache import cache
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from mailings.forms import MailingRecipientForm, MessageForm, MailingForm
from mailings.models import MailingRecipient, Message, Mailing
from mailings.services import send_mailing


class HomeView(View):
    template_name = 'mailings/home.html'

    def get(self, request):
        mailings = Mailing.objects.count()
        mailings_active = Mailing.objects.filter(status=Mailing.LAUNCHED).count()
        unique_recipients = MailingRecipient.objects.count()
        context = {
            'total_mailings': mailings,
            'unique_recipients': unique_recipients,
            'mailings_active': mailings_active
        }

        return render(request, self.template_name, context)


class MailingRecipientsListView(ListView):
    model = MailingRecipient


class MailingRecipientCreateView(CreateView):
    template_name = 'mailings/mailing_recipient_form.html'
    form_class = MailingRecipientForm
    success_url = reverse_lazy('mailings:mailing_recipients_list')


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingRecipientDetailView(DetailView):
    model = MailingRecipient


class MailingRecipientUpdateView(UpdateView):
    template_name = 'mailings/mailing_recipient_form.html'
    model = MailingRecipient
    form_class = MailingRecipientForm
    success_url = reverse_lazy('mailings:mailing_recipients_list')

    def get_success_url(self):
        return reverse('mailings:mailing_recipient_detail', args=[self.kwargs.get('pk')])


class MessageListView(ListView):
    model = Message


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingRecipientDeleteView(DeleteView):
    model = MailingRecipient
    template_name = 'mailings/confirm_delete.html'
    success_url = reverse_lazy('mailings:mailing_recipients_list')


class MessageCreateView(CreateView):
    template_name = 'mailings/message_form.html'
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')


@method_decorator(cache_page(60 * 15), name='dispatch')
class MessageDetailView(DetailView):
    model = Message


class MessageUpdateView(UpdateView):
    template_name = 'mailings/message_form.html'
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')

    def get_success_url(self):
        return reverse('mailings:message_detail', args=[self.kwargs.get('pk')])


class MessageDeleteView(DeleteView):
    template_name = 'mailings/confirm_delete.html'
    model = Message
    success_url = reverse_lazy('mailings:message_list')


class MailingsListView(ListView):
    model = Mailing

    def get_queryset(self):
        queryset = cache.get('my_queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('my_queryset', queryset, 60 * 15)  # Кешируем данные на 15 минут
        return queryset


class MailingCreateView(CreateView):
    template_name = 'mailings/mailing_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailings_list')


class MailingDetailView(DetailView):
    model = Mailing


class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = 'mailings/mailing_form.html'
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailings_list')

    def get_success_url(self):
        return reverse('mailings:mailing_detail', args=[self.kwargs.get('pk')])


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailings/confirm_delete.html'
    success_url = reverse_lazy('mailings:mailings_list')


class SendMailingView(View):

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, id=pk)
        send_mailing(mailing)
        return redirect('/')
