from django.shortcuts import render
from django.views.generic import DetailView, ListView

from blog.models import Blog


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):  # счетчик просмоитров
        self.object = super().get_object(queryset)  # возвращает объект с перемеными
        self.object.count_of_view += 1  # увеличивает счетчик просмотров
        self.object.save()  # сохраняет изменения
        return self.object

class BlogListView(ListView):
    model = Blog