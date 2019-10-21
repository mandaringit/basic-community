from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label="", help_text="🤬 악플은 지양해주세요", widget=forms.TextInput(attrs={'placeholder': "댓글을 써주세요"}))

    class Meta:
        model = Comment
        fields = ['content']
