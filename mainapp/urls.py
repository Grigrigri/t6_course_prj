from django.urls import path, include
from mainapp import views

urlpatterns = [

    path("", views.Home.as_view()),

    path("filter/", views.FilterPostsView.as_view(), name = 'filter'),
    path("search/", views.EasyFullTextSearch.as_view(), name = 'search'),

    path("posts/<int:pk>/", views.PostView.as_view(), name = 'post'),
    path("posts/", views.AllPostsView.as_view(), name = 'posts'),
    
    path("categories/<slug:slug>/", views.CategoryView.as_view(), name = 'category'),

    path("authors/<slug:slug>/", views.AuthorView.as_view(), name = 'author'),
    path("authors/", views.AllAuthorsView.as_view(), name = 'authors'),

    path("comments/<int:pk>/", views.AddComment.as_view(), name = 'add_comment'),

    path("ratings/", include('star_ratings.urls', namespace='ratings'), name='ratings'),

]
