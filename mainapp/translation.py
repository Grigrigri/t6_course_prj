from modeltranslation.translator import register, TranslationOptions
from .models import Categories, Authors, Countries, Genres, Posts, PostImages

@register(Categories)
class CategoriesTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Countries)
class CountriesTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Authors)
class AuthorsTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Genres)
class GenresTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Posts)
class PostsTranslationOptions(TranslationOptions):
    fields = ('title', 'text')

@register(PostImages)
class PostImagesTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

