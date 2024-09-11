from django import forms
from .models import Meme, Comment


class MemeForm(forms.ModelForm):

    class Meta:
        model = Meme
        fields = ['title', 'image']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']
