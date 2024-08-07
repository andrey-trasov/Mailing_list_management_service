from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from blog.models import Blog
from mailings.forms import ClientForm, MessageForm, NewsletterForm, NewsletterModeratorForm
from mailings.models import Client, Message, Newsletter, Logs


# Клиенты
class ClientListView(ListView):
    model = Client

    def get_queryset(self, *args, **kwargs):
        """
        показывает только клиентов созданных пользователем
        """
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(owner=self.request.user)
        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user  # получаю авторизованного пользователя
        product.owner = user
        product.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ['email', 'fio', 'comment']
    success_url = reverse_lazy('mailings:client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailings:client_list')


class ClientDetailView(DetailView):
    model = Client


# Сообщения
class MessageListView(ListView):
    model = Message

    def get_queryset(self, *args, **kwargs):
        """
        показывает только сообщения созданные пользователем
        """
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(owner=self.request.user)
        return queryset


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    forms = MessageForm
    fields = ['subject', 'body', ]
    success_url = reverse_lazy('mailings:message_list')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user  # получаю авторизованного пользователя
        product.owner = user
        product.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ['subject', 'body']
    success_url = reverse_lazy('mailings:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailings:message_list')


class MessageDetailView(DetailView):
    model = Message


# Рассылка

class NewsletterListView(ListView):
    model = Newsletter

    def get_queryset(self, *args, **kwargs):
        """
        показывает только рассылки созданные пользователем и админам
        """
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user  # получаем юзера
        if user.has_perm('mailings.сan_view_any_mailing_lists'):  # если имеет эти права
            return queryset  # возвращаем форму для модераторов
        queryset = queryset.filter(owner=user)
        return queryset

    def post(self, request, *args, **kwargs):
        mailing = Newsletter.objects.filter(pk=request.POST.get('status')).first()
        print(mailing)
        if mailing.is_active:
            mailing.is_active = False
        else:
            mailing.is_active = True
        mailing.save()
        return redirect('mailings:newsletter_list')


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('mailings:client_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = Newsletter(owner=self.request.user)
        return kwargs

    def form_valid(self, form):
        product = form.save(commit=False)
        user = self.request.user  # получаю авторизованного пользователя
        product.owner = user
        product.save()
        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    success_url = reverse_lazy('mailings:client_list')

    def get_form_class(self):
        user = self.request.user  # получаем юзера
        if user == self.object.owner:  # если юзер является хозяином магазина
            return NewsletterForm  # возвращаем обычную форму
        if user.has_perm('mailings.can_disable_mailing_lists'):  # если имеет эти права
            return NewsletterModeratorForm  # возвращаем форму для модераторов
        raise PermissionDenied  # выдает ошибку 403


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    model = Newsletter
    success_url = reverse_lazy('mailings:client_list')


class NewsletterDetailView(DetailView):
    model = Newsletter


# логи
class LogsListView(ListView):
    model = Logs

    def get_queryset(self, *args, **kwargs):
        """
        показывает только логи пользовательских рассылок или админам все рассылки
        """
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user  # получаем юзера
        if user.has_perm('mailings.сan_view_any_mailing_lists'):  # если имеет эти права
            return queryset  # возвращаем форму для модераторов
        queryset = queryset.filter(owner=user)
        return queryset


class BlogListView(ListView):
    model = Blog


def index_data(request):
    count_mailing_items = Newsletter.objects.count()
    count_active_mailing_items = Newsletter.objects.filter(status='launched').count()
    clients = Client.objects.all()
    emails = []
    for client in clients:
        emails.append(client.email)
    count_unic_clients = len(set(emails))
    random_blogs = Blog.objects.order_by('?')[:3]
    context = {'count_mailing_items': count_mailing_items,
               'count_active_mailing_items': count_active_mailing_items,
               'count_unic_clients': count_unic_clients,
               'random_blogs': random_blogs,
               }

    return render(request, 'mailings/index.html', context)
