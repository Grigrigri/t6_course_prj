from django import template
from ..models import Categories, Countries, Authors, Genres, Posts, PostRating

register = template.Library()

@register.simple_tag()
def get_categories():
	return Categories.objects.all()

@register.simple_tag()
def get_authors():
	return Authors.objects.all()

@register.simple_tag()
def get_genres():
	return Genres.objects.all()

@register.simple_tag()
def get_countries():
	return Countries.objects.all()

@register.inclusion_tag('mainapp/last_posts.html')
def get_last_posts(count = 9):
	posts = Posts.objects.filter(draft = False).only("title", "poster", "text", "iuser", "date") [:count]
	return {"last_posts" : posts}

@register.inclusion_tag('mainapp/all_posts.html')
def get_all_posts():
	posts = Posts.objects.filter(draft = False).only("title", "poster", "text", "iuser", "date")
	return {"posts" : posts}