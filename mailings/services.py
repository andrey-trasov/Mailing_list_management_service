from datetime import datetime
from random import shuffle

import pytz
from django.core.cache import cache

from myproject import settings
from myproject.settings import CACHE_ENABLED
from mailings.models import Client, Newsletter
from blog.models import Blog


def get_datetime():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    return current_datetime


def get_uniq_clients_count():
    if CACHE_ENABLED:
        key = 'uniq_clients_count'
        uniq_clients_count = cache.get(key)
        if uniq_clients_count is None:
            clients = Client.objects.all()
            email_list = []
            for client in clients:
                email_list.append(client.email)
            uniq_clients_count = len(set(email_list))
            cache.set(key, uniq_clients_count, timeout=60)
    else:
        clients = Client.objects.all()
        email_list = []
        for client in clients:
            email_list.append(client.email)
        uniq_clients_count = len(set(email_list))
    return uniq_clients_count


def count_mailing_items():
    if not CACHE_ENABLED:
        return Newsletter.objects.count()
    key = 'category_list'
    mailings = cache.get(key)
    if mailings is not None:
        return mailings
    mailings = Newsletter.objects.count()
    cache.set(key, mailings)
    return mailings


def count_active_mailing_items():
    if not CACHE_ENABLED:
        return Newsletter.objects.filter(status='launched').count()
    key = 'category_list_active'
    mailings = cache.get(key)
    if mailings is not None:
        return mailings
    mailings = Newsletter.objects.filter(status='launched').count()
    cache.set(key, mailings)
    return mailings


def get_random_blogs():
    if CACHE_ENABLED:
        key = 'random_blogs'
        random_blogs = cache.get(key)
        if random_blogs is None:
            random_blogs = list(Blog.objects.order_by('?')[:12])
            cache.set(key, random_blogs, timeout=60)
    else:
        random_blogs = list(Blog.objects.order_by('?')[:12])
    shuffle(random_blogs)
    return random_blogs[:3]


