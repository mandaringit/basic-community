from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .models import Post
# Create your views here.


def index(req):
    posts = Post.objects.all()
    return render(req, 'posts/index.html', {'posts': posts})


@login_required
def create(req):
    user = req.user
    if req.method == "POST":
        form = PostForm(req.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user
            post.save()
            return redirect('posts:index')
    else:
        form = PostForm()
    return render(req, 'posts/form.html', {'form': form})


def detail(req, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(req, 'posts/detail.html', {'post': post})


def update(req, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = req.user

    if post.user != user:
        return redirect('posts:detail', post_id)
    else:
        if req.method == "POST":
            form = PostForm(req.POST, instance=post)
            if form.is_valid():
                form.save()
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
