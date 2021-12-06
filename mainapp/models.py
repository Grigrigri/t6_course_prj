from django.db import models
from datetime import date
from django.urls import reverse
from django.contrib.auth.models import User


class Categories(models.Model):
	name = models.CharField("category", max_length = 100)
	description = models.TextField("description")
	url = models.SlugField(max_length = 160, unique = True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("category", kwargs = {"slug" : self.url})

	class Meta:
		verbose_name = "category"
		verbose_name_plural = "category"

class Authors(models.Model):
	name = models.CharField("author", max_length = 100)
	description = models.TextField("description")
	photo = models.ImageField("photo", upload_to = "authors/")
	url = models.SlugField(max_length = 160, unique = True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("author", kwargs = {"slug" : self.url})

	class Meta:
		verbose_name = "author"
		verbose_name_plural = "author"

class Countries(models.Model):
	name = models.CharField("country", max_length = 30)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "country"
		verbose_name_plural = "country"

class Genres(models.Model):
	name = models.CharField("genre", max_length = 100)
	description = models.TextField("description")
	url = models.SlugField(max_length = 160, unique = True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "genre"
		verbose_name_plural = "genre"

class Posts(models.Model):
	title = models.CharField("post", max_length = 100)
	text = models.TextField("text", max_length = 5000)
	poster = models.ImageField("poster", upload_to = "posters/")

	iuser = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True, verbose_name="name", related_name = "content_user")

	country = models.ManyToManyField(Countries, verbose_name = "country", related_name = "content_country")
	author = models.ManyToManyField(Authors, verbose_name = "author", related_name = "content_author")
	genre = models.ManyToManyField(Genres, verbose_name = "genre", related_name = "content_genre")

	category = models.ForeignKey(
		Categories, verbose_name = "category", related_name = "content_category", on_delete = models.SET_NULL, null = True
	)

	date = models.DateField("date", default = date.today)
	draft = models.BooleanField("draft", default = False)
	url = models.SlugField(max_length = 160, unique = True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("post", kwargs = {"pk" : self.id})

	class Meta:
		verbose_name = "post"
		verbose_name_plural = "post"
		ordering = ['-id']

class PostImages(models.Model):
	title = models.CharField("post_image", max_length = 30)
	description = models.TextField("description")
	image = models.ImageField("image", upload_to = "post_images/")

	post = models.ForeignKey(
		Posts, on_delete = models.CASCADE, verbose_name = "post"
	)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "post_image"
		verbose_name_plural = "post_image"

class Rating(models.Model):
	value = models.PositiveSmallIntegerField("star", default = 0)

	def __str__(self):
		return f'{self.value}'

	class Meta:
		verbose_name = "star"
		verbose_name_plural = "star"
		ordering = ['-value']


class PostRating(models.Model):
	ip = models.CharField("ip", max_length = 15)

	star = models.ForeignKey(
		Rating, on_delete = models.CASCADE, verbose_name = "star"
	)

	post = models.ForeignKey(
		Posts, on_delete = models.CASCADE, verbose_name = "post"
	)

	def __str__(self):
		return f"{self.star} - {self.post}"

	class Meta:
		verbose_name = "post_rating"
		verbose_name_plural = "post_rating"

class Comments(models.Model):
	iuser = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True, verbose_name="iuser", related_name = "comments_user")
	text = models.TextField("text", max_length = 1000)
	date = models.DateField("date", default = date.today)
	
	post = models.ForeignKey(
		Posts, on_delete = models.CASCADE, verbose_name = "post"
	)

	def __str__(self):
		return f"{self.iuser} - {self.post}"

	class Meta:
		verbose_name = "comments"
		verbose_name_plural = "comments"