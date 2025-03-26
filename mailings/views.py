from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from mailings.models import MailingRecipient, Message, Mailing


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
    model = MailingRecipient
    fields = '__all__'
    success_url = reverse_lazy('mailings:mailing_recipients_list')


class MailingRecipientDetailView(DetailView):
    model = MailingRecipient


class MailingRecipientUpdateView(UpdateView):
    template_name = 'mailings/mailing_recipient_form.html'
    model = MailingRecipient
    fields = '__all__'
    success_url = reverse_lazy('mailings:mailing_recipients_list')

    def get_success_url(self):
        return reverse('mailings:mailing_recipient_detail', args=[self.kwargs.get('pk')])


class MessageListView(ListView):
    model = Message


class MailingRecipientDeleteView(DeleteView):
    model = MailingRecipient
    template_name = 'mailings/confirm_delete.html'
    success_url = reverse_lazy('mailings:mailing_recipients_list')


class MessageCreateView(CreateView):
    template_name = 'mailings/message_form.html'
    model = Message
    fields = '__all__'
    success_url = reverse_lazy('mailings:message_list')


class MessageDetailView(DetailView):
    model = Message


class MessageUpdateView(UpdateView):
    template_name = 'mailings/message_form.html'
    model = Message
    fields = '__all__'
    success_url = reverse_lazy('mailings:message_list')

    def get_success_url(self):
        return reverse('mailings:message_detail', args=[self.kwargs.get('pk')])


class MessageDeleteView(DeleteView):
    template_name = 'mailings/confirm_delete.html'
    model = Message
    success_url = reverse_lazy('mailings:message_list')


class MailingsListView(ListView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    template_name = 'mailings/mailing_form.html'
    fields = '__all__'
    success_url = reverse_lazy('mailings:mailings_list')


class MailingDetailView(DetailView):
    model = Mailing


class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = 'mailings/mailing_form.html'
    fields = '__all__'
    success_url = reverse_lazy('mailings:mailings_list')

    def get_success_url(self):
        return reverse('mailings:mailing_detail', args=[self.kwargs.get('pk')])


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailings/confirm_delete.html'
    success_url = reverse_lazy('mailings:mailings_list')
