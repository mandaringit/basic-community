from django.shortcuts import render, redirect
from .forms import PostForm
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(req):
    return render(req, 'posts/index.html')


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
