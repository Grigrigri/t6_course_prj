from django import template
from ..models import Categories, Posts, PostRating

register = template.Library()

@register.simple_tag()
def get_categories():
	return Categories.objects.all()

@register.inclusion_tag('mainapp/last_posts.html')
def get_last_posts(count = 9):
	posts = Posts.objects.filter(draft = False).only("title", "poster", "text", "user", "date") [:count]
	return {"last_posts" : posts}

@register.inclusion_tag('mainapp/all_posts.html')
def get_all_posts():
	posts = Posts.objects.filter(draft = False).only("title", "poster", "text", "user", "date")
	return {"posts" : posts}