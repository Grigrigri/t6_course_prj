from django.shortcuts import render, redirect

from django.views.generic.base import View
from django.views.generic import ListView, DetailView

from django.db.models import Q

from .models import Categories, Authors, Countries, Genres, Posts, PostImages, Rating, PostRating, Comments
from .forms import CommentForm, AddPostForm

from django.contrib.postgres.search import SearchVector
from django.db.models import Avg

from django.template import RequestContext



#Errors

def handler_404(request, exception):
   context = {}
   return render(request,'mainapp/404.html', context)

def handler_500(request):
   context = {}
   return render(request,'mainapp/500.html', context)



#Filter

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



#Search

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



#Home

class Home(СriteriaFilter, ListView):
    model = Posts
    template_name = "mainapp/home.html"



#Posts

class AllPostsView(СriteriaFilter, ListView):
    model = Posts
    queryset = Posts.objects.filter(draft = False).only("title", "poster", "text", "iuser", "date")
    template_name = "mainapp/posts.html"

    paginate_by = 9

class MyPostsView(СriteriaFilter, ListView):
    model = Posts
    queryset = Posts.objects.filter(draft = False).only("title", "poster", "text", "iuser", "date")
    template_name = "mainapp/user_posts.html"

    paginate_by = 9

class PostView(СriteriaFilter, DetailView):
    model = Posts
    slug_field = "url"
    template_name = "mainapp/post.html"
    
    # old rating

    def get_rating(self):
        value = PostRating.objects.filter(post = self.kwargs['pk']).aggregate(Avg('star'))
        return value

class PostAddView(СriteriaFilter, ListView): #CreateView
    model = Posts
    form_class = AddPostForm
    template_name = "mainapp/post_add.html"
    
class PostEditView(СriteriaFilter, DetailView):
    model = Posts
    slug_field = "url"
    template_name = "mainapp/post_edit.html"

# Posts, methods

def post_add(request):
    try:

        if request.method == "POST":
            post = Posts()
            post.title_ru = request.POST.get("title_ru")
            post.title_en = request.POST.get("title_en")

            post.text_ru = request.POST.get("text_ru")
            post.text_en = request.POST.get("text_en")

            post.iuser = request.POST.get("iuser")

            post.country.set(request.POST.get('country')) 

            #post.country.set(Countries.objects.filter(id = request.POST.get("country"))) 
            post.author = request.POST.get("author")
            post.genre = request.POST.get("genre")
            post.category = request.POST.get("category")

            post.url = request.POST.get("url")

            post.save()
        return redirect('/user_posts')
    except Posts.DoesNotExist:
        return redirect('/user_posts')

def post_edit(request, pk):
    try:
        post = Posts.objects.get(id = pk)
        return redirect('/user_posts')
    except Posts.DoesNotExist:
        return redirect('/user_posts')

def post_delete(request, pk):
    try:
        post = Posts.objects.get(id = pk)
        post.delete()
        return redirect('/user_posts')
    except Posts.DoesNotExist:
        return redirect('/user_posts')



#Comments

class MyCommentsView(СriteriaFilter, ListView):
    model = Comments
    queryset = Comments.objects.only("text", "date", "post")
    template_name = "mainapp/user_comments.html"

    paginate_by = 9

class AddComment(View):

    def post(self, request, pk):
        form = CommentForm(request.POST)
        post = Posts.objects.get(id = pk)
        if form.is_valid():
            form = form.save(commit = False)
            form.post = post
            form.save()
        return redirect(post.get_absolute_url())



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



#Categories

class CategoryView(СriteriaFilter, DetailView):
   
    model = Categories 
    slug_field = "url"
    template_name = "mainapp/category.html"