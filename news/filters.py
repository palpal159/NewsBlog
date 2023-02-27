from django_filters import FilterSet, DateFilter
from django import forms
from .models import Post


class PostFilter(FilterSet):
    date_time_post = DateFilter('date_time_post__date', label='Найти посты по заданной дате')

    class Meta:
        model = Post
        fields = {
            'type_post': ['exact'],
            'author_post': ['exact'],
            'categories_post': ['exact'],
        }
        widget = forms.DateInput()

#по названию
#по тегу
#по дате