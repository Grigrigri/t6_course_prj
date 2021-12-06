from django.urls import path, include
from mainapp import views

urlpatterns = [

    path("", views.Home.as_view()),

    path("filter/", views.FilterPostsView.as_view(), name = 'filter'),
    path("search/", views.EasyFullTextSearch.as_view(), name = 'search'),

    path("posts/add", views.PostAddView.as_view()),
    path("posts/add/save", views.post_add, name = 'add_post'),

    path("posts/<int:pk>/", views.PostView.as_view(), name = 'post'),

    path("posts/<int:pk>/edit", views.PostEditView.as_view(), name = 'post_edit'),
    path("posts/<int:pk>/delete", views.post_delete),

    path("posts/", views.AllPostsView.as_view(), name = 'posts'),

    path("user_posts/", views.MyPostsView.as_view(), name = 'user_posts'),
    path("user_comments/", views.MyCommentsView.as_view(), name = 'user_comments'),
    
    path("categories/<slug:slug>/", views.CategoryView.as_view(), name = 'category'),

    path("authors/<slug:slug>/", views.AuthorView.as_view(), name = 'author'),
    path("authors/", views.AllAuthorsView.as_view(), name = 'authors'),

    path("comments/<int:pk>/", views.AddComment.as_view(), name = 'add_comment'),

    path("ratings/", include('star_ratings.urls', namespace='ratings'), name='ratings'),

]
