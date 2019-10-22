from django.db import models
from django.conf import settings
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    post_img = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_posts')


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    comment_img = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_comments')
