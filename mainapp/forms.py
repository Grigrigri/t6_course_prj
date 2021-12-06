from django import forms

from .models import Comments, Posts



class CommentForm(forms.ModelForm):
	class Meta:
		model = Comments
		fields = ('iuser', 'text')



class AddPostForm(forms.ModelForm):
 
    class Meta:
        model = Posts
        fields = [ 'title_ru', 'title_en', 'text_ru', 'text_en', 'poster', 'iuser',
        'country', 'author', 'genre', 'category', 'date', 'draft', 'url' ]

