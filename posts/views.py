from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Hashtag
from django.core.paginator import Paginator
import random
from django.http import JsonResponse
# Create your views here.

# Utility fn


def hashtagging(obj):
    for word in obj.content.split():
        if word.startswith('#'):
            hashtag, created = Hashtag.objects.get_or_create(
                content=word)
            obj.hashtags.add(hashtag)

# routes


def index(req):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 12)

    page = req.GET.get('page')
    posts = paginator.get_page(page)
    return render(req, 'posts/index.html', {'posts': posts})


@login_required
def create(req):
    user = req.user
    if req.method == "POST":
        form = PostForm(req.POST, req.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user
            post.save()

            # 해시태그 작업 (구체적인 방법은 수정 필요.)
            hashtagging(post)

            return redirect('posts:index')
    else:
        form = PostForm()
    return render(req, 'posts/form.html', {'form': form})


def detail(req, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment_form = CommentForm()
    return render(req, 'posts/detail.html', {'post': post, 'comment_form': comment_form})


def update(req, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = req.user

    if post.user != user:
        return redirect('posts:detail', post_id)
    else:
        if req.method == "POST":
            form = PostForm(req.POST, req.FILES, instance=post)
            if form.is_valid():
                post = form.save()
                # 해시태그 재작업 필요함
                post.hashtags.clear()
                hashtagging(post)

                return redirect('posts:detail', post_id)
        else:
            form = PostForm(instance=post)

        return render(req, 'posts/form.html', {'form': form})


def delete(req, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user != req.user:
        return redirect('posts:detail', post_id)
    else:
        post.delete()

    return redirect('posts:index')


def comments_create(req, post_id):
    post = get_object_or_404(Post, id=post_id)

    if req.user.is_authenticated:
        user = req.user
        if req.method == "POST":
            form = CommentForm(req.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.user = user
                comment.save()

                # 해시태그 작업
                hashtagging(comment)

                return redirect('posts:detail', post_id)
    else:
        return redirect('posts:detail', post_id)


def comments_delete(req, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if req.user == comment.user:
        comment.delete()

    return redirect('posts:detail', post_id)


def comments_update(req, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if req.user == comment.user:

        if req.method == "POST":
            form = CommentForm(req.POST, instance=comment)
            if form.is_valid():
                form.save()
                comment.hashtags.clear()
                hashtagging(comment)
                return redirect('posts:detail', post_id)
        else:
            form = CommentForm(instance=comment)

        return render(req, 'posts/form.html', {'form': form})
    else:
        return redirect('posts:detail', post_id)


@login_required
def post_like(req, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = req.user

    if user in post.like_users.all():
        post.like_users.remove(user)
        is_post_liked = False
    else:
        post.like_users.add(user)
        is_post_liked = True

    post_like_count = post.like_users.all().count()

    context = {
        'is_post_liked': is_post_liked,
        'post_like_count': post_like_count
    }

    return JsonResponse(context)


@login_required
def comment_like(req, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = req.user

    if comment.like_users.filter(id=user.id):
        comment.like_users.remove(user)
        is_comment_liked = False
    else:
        comment.like_users.add(user)
        is_comment_liked = True

    comment_like_count = comment.like_users.all().count()
    context = {
        'is_comment_liked': is_comment_liked,
        'comment_like_count': comment_like_count
    }

    return JsonResponse(context)


def hashtag(req, tag_id):
    hashtag = get_object_or_404(Hashtag, id=tag_id)

    return render(req, 'posts/hashtag.html', {'hashtag': hashtag})
