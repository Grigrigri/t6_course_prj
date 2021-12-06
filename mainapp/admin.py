from django.contrib import admin
from .models import Categories, Authors, Countries, Genres, Posts, PostImages, Rating, PostRating, Comments
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from modeltranslation.admin import TranslationAdmin

admin.site.site_title = "Django Reccomend."
admin.site.site_header = "Django Reccomend."

class PostsAdminForm(forms.ModelForm):
    
    text_ru = forms.CharField(label="Description", widget=CKEditorUploadingWidget())
    text_en = forms.CharField(label="Description", widget=CKEditorUploadingWidget())

    class Meta:
        model = Posts
        fields = '__all__'

@admin.register(Categories)
class CategoriesAdmin(TranslationAdmin):
	list_display = ("id", "name", "url")
	list_display_links = ("name", )

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
	list_display = ("id", "iuser", "post")
	readonly_fields = ("iuser",)

class CommentsInline(admin.StackedInline):
	model = Comments
	extra = 1
	readonly_fields = ("iuser", "post",)

class PostImagesInline(admin.StackedInline):
	model = PostImages
	extra = 1

	readonly_fields = ("get_image",)

	def get_image(self, obj):
		return mark_safe(f'<img src = {obj.image.url} width = "75" height = "90"')

	get_image.short_description = "image"

@admin.register(Posts)
class PostsAdmin(TranslationAdmin):
	list_display = ("get_poster", "title", "category", "url", "draft")
	list_filter = ("category", "country", "author", "genre", )
	search_fields = ("title", "category__name", "country__name", "author__name", "genre__name",)
	inlines = [ PostImagesInline, CommentsInline]
	save_on_top = True
	save_as = True
	list_editable = ("draft", )

	def save_model(self, request, obj, form, change):
	      if form.is_valid():
	         if not request.user.is_superuser or not form.cleaned_data["iuser"]:
	            obj.iuser = request.user
	            obj.save()
	         elif form.cleaned_data["iuser"]:
	            obj.iuser = form.cleaned_data["iuser"]
	            obj.save()


	actions = ["publish", "unpublish"]
	form = PostsAdminForm

	readonly_fields = ("get_poster",)

	def get_poster(self, obj):
		return mark_safe(f'<img src = {obj.poster.url} width = "50" height = "60"')

	def unpublish(self, request, queryset):
		row_update = queryset.update(draft = True)

		if row_update == '1':
			message = "one post was update"
		else:
			message = f"{row_update} posts were update"

		self.message_user(request, f"{message}")

	def publish(self, request, queryset):
		row_update = queryset.update(draft = False)
		
		if row_update == '1':
			message = "one post was update"
		else:
			message = f"{row_update} posts were update"

		self.message_user(request, f"{message}")

	publish.short_description = "Published"
	publish.allowed_permissions = ('change',)

	unpublish.short_description = "Unpublished"
	unpublish.allowed_permissions = ('change',)

	get_poster.short_description = "poster"

@admin.register(Authors)
class AuthorsAdmin(TranslationAdmin):
	list_display = ("get_photo", "name",)
	search_fields = ("name",)
	readonly_fields = ("get_photo",)
	def get_photo(self, obj):
		return mark_safe(f'<img src = {obj.photo.url} width = "50" height = "60"')

	get_photo.short_description = "photo"


@admin.register(Countries)
class CountriesAdmin(TranslationAdmin):
	list_display = ("name",)

@admin.register(Genres)
class GenresAdmin(TranslationAdmin):
	list_display = ("name",)

@admin.register(PostImages)
class PostImagesAdmin(TranslationAdmin):
	list_display = ("get_image", "title",)
	readonly_fields = ("get_image",)

	def get_image(self, obj):
		return mark_safe(f'<img src = {obj.image.url} width = "50" height = "60"')

	get_image.short_description = "image"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
	list_display = ("value",)

@admin.register(PostRating)
class PostRatingAdmin(admin.ModelAdmin):
	list_display = ("ip",)

