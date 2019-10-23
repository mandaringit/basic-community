from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
# Create your views here.


@login_required
def mypage(req):
    user = req.user

    return render(req, 'accounts/mypage.html', {'user': user})


def signup(req):
    if req.user.is_authenticated:
        return redirect('posts:index')

    if req.method == 'POST':
        form = CustomUserCreationForm(req.POST)
        if form.is_valid():
            user = form.save()
            auth_login(req, user)
            return redirect('posts:index')
    else:
        form = CustomUserCreationForm()
    return render(req, 'accounts/form.html', {'form': form})


def login(req):
    if req.user.is_authenticated:
        return redirect('posts:index')

    if req.method == "POST":  # 인증만 하는 것이기 때문에 form.get_user로 유저 정보를 가져와야함
        form = AuthenticationForm(req, req.POST)
        if form.is_valid():
            auth_login(req, form.get_user())
            return redirect(req.GET.get('next') or 'posts:index')
    else:
        form = AuthenticationForm()

    return render(req, 'accounts/form.html', {'form': form})


def logout(req):
    auth_logout(req)
    return redirect('posts:index')
