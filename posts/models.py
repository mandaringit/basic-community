from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail, ResizeToFill


class Hashtag(models.Model):
    content = models.CharField(max_length=100)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    post_img = ProcessedImageField(
        processors=[ResizeToFill(300, 300)],
        format='GIF',
        options={'quality': 90},
        upload_to='media')
    created_at = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_posts')
    hashtags = models.ManyToManyField(Hashtag, related_name="posts")


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    comment_img = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_comments')
    hashtags = models.ManyToManyField(Hashtag, related_name="comments")
