from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):

    title = forms.CharField(label='제목')
    content = forms.CharField(widget=forms.Textarea, label='내용')
    post_img = forms.CharField(required=False,
                               label="URL", help_text="이미지 주소를 넣어주세요", widget=forms.TextInput(attrs={'placeholder': "IMAGE URL"}))

    class Meta:
        model = Post
        fields = ['title', 'content', 'post_img']


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label="", help_text="🤬 악플은 지양해주세요", widget=forms.TextInput(attrs={'placeholder': "댓글을 써주세요"}))
    comment_img = forms.CharField(required=False,
                                  label="", help_text="이미지 주소를 넣어주세요", widget=forms.TextInput(attrs={'placeholder': "IMAGE URL(필수는 아니에요)"}))

    class Meta:
        model = Comment
        fields = ['content', 'comment_img']
