from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Category
from .filters import PostFilter
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


@login_required
def subscribe(request, pk):
    user = request.user
    cat = Category.objects.get(id=pk)
    cat.subscribers.add(user)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe(request, pk):
    user = request.user
    cat = Category.objects.get(id=pk)
    cat.subscribers.remove(user)
    return redirect(request.META.get('HTTP_REFERER'))


class BaseView(TemplateView):
    template_name = 'base.html'


class PostList(ListView):
    model = Post
    ordering = ['-date_time_post']
    template_name = 'posts.html'
    context_object_name = 'post_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostSearch(ListView):
    model = Post
    ordering = ['-date_time_post']
    template_name = 'post_search.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post_list'


class NewsCreate(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    permission_required = ('news.add_news', 'news.update_news')
    success_url = reverse_lazy('post_id:id')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        user = request.user
        if form.is_valid():
            post = form.save(commit=False)
            post.author_post = Author.objects.first()
            post.save()
            return self.form_valid(form)
        else:
            return self.form_valid(form)


class ArticlesCreate(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'articles_create.html'
    permission_required = ('articles.add_articles', 'articles.update_articles')
    success_url = reverse_lazy('post_id:id')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        user = request.user
        if form.is_valid():
            post = form.save(commit=False)
            post.author_post = Author.objects.first()
            post.save()
            return self.form_valid(form)

        return self.form_valid(form)


class NewsUpdate(UpdateView, LoginRequiredMixin, TemplateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'


class ArticlesUpdate(UpdateView, LoginRequiredMixin, TemplateView):
    form_class = PostForm
    model = Post
    template_name = 'articles_create.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('post_list')
