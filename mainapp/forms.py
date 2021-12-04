from django import forms

from .models import Comments, Rating, PostRating

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comments
		fields = ('name', 'email', 'text')