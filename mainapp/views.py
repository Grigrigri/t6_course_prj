from django.shortcuts import render, redirect

from django.views.generic.base import View
from django.views.generic import ListView, DetailView

from django.db.models import Q

from .models import Categories, Authors, Countries, Genres, Posts, PostImages, Rating, PostRating, Comments
from .forms import CommentForm

from django.contrib.postgres.search import SearchVector
from django.db.models import Avg

class СriteriaFilter:
    def get_genres(self):
        return Genres.objects.all()

class FilterPostsView(СriteriaFilter, ListView):
    template_name = "mainapp/posts.html"

    def get_queryset(self):
        queryset = Posts.objects.filter(
            Q(genre__in = self.request.GET.getlist("genre"))
        ).distinct()
        return queryset

class EasyFullTextSearch(ListView):

    template_name = "mainapp/posts.html"

    def get_queryset(self):
        return Posts.objects.annotate(
            search=SearchVector('title', 'text', 'comments'),
            ).filter(search = self.request.GET.get("q"))

class SearchPosts(ListView):

    template_name = "mainapp/posts.html"

    def get_queryset(self):
        return Posts.objects.filter(
            Q(title__icontains = self.request.GET.get("q")) |
            Q(text__icontains = self.request.GET.get("q"))
            )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.getlist("q")
        return context

class AddComment(View):

    def post(self, request, pk):
        form = CommentForm(request.POST)
        post = Posts.objects.get(id = pk)
        if form.is_valid():
            form = form.save(commit = False)
            form.post = post
            form.save()
        return redirect(post.get_absolute_url())

class Home(СriteriaFilter, ListView):
    model = Posts
    template_name = "mainapp/home.html"

class AllPostsView(СriteriaFilter, ListView):
    model = Posts
    queryset = Posts.objects.filter(draft = False).only("title", "poster", "text", "user", "date")
    template_name = "mainapp/posts.html"
    paginate_by = 9

class PostView(СriteriaFilter, DetailView):
    model = Posts
    slug_field = "url"
    template_name = "mainapp/post.html"
    
    def get_rating(self):
        value = PostRating.objects.filter(post = self.kwargs['pk']).aggregate(Avg('star'))
        return value

#Authors

class AllAuthorsView(СriteriaFilter, ListView):
    model = Authors
    queryset = Authors.objects.all().only("name", "photo", "description")
    template_name = "mainapp/authors.html"
    paginate_by = 9

class AuthorView(СriteriaFilter, DetailView):
    model = Authors
    slug_field = "url"
    template_name = "mainapp/author.html"

class CategoryView(СriteriaFilter, DetailView):
    model = Categories 
    slug_field = "url"
    template_name = "mainapp/category.html"

