from django.shortcuts import render
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


class MailingRecipientDetailView(DetailView):
    model = MailingRecipient


class MailingRecipientUpdateView(UpdateView):
    template_name = 'mailings/mailing_recipient_form.html'
    model = MailingRecipient
    fields = '__all__'


class MailingRecipientDeleteView(DeleteView):
    model = MailingRecipient
    template_name = 'mailings/mailing_recipient_form.html'


class MessageCreateView(CreateView):
    template_name = 'mailings/message_form.html'
    model = Message
    fields = '__all__'


class MessageDetailView(DetailView):
    model = Message


class MessageUpdateView(UpdateView):
    template_name = 'mailings/message_form.html'
    model = Message


class MessageDeleteView(DeleteView):
    template_name = 'mailings/message_form.html'
    model = Message


class MailingsListView(ListView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    template_name = 'mailings/mailing_form.html'
    fields = '__all__'


class MailingDetailView(DetailView):
    model = Mailing


class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = 'mailings/mailing_form.html'
    fields = '__all__'


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_form.html'
