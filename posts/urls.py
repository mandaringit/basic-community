from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:post_id>/', views.detail, name='detail'),
    path('<int:post_id>/update/', views.update, name='update'),
    path('<int:post_id>/delete/', views.delete, name='delete'),

    path('<int:post_id>/comments/create/',
         views.comments_create, name='comments_create'),
    path('<int:post_id>/comments/<int:comment_id>/delete/',
         views.comments_delete, name="comments_delete"),
    path('<int:post_id>/comments/<int:comment_id>/update/',
         views.comments_update, name="comments_update"),
    path('<int:post_id>/like/', views.post_like, name='post_like'),
    path('<int:post_id>/comments/<int:comment_id>/like',
         views.comment_like, name='comment_like'),
    path('hashtags/<int:tag_id>/', views.hashtag, name='hashtag')
]
