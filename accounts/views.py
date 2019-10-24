from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User
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


@login_required  # 포스트 요구 ? 로그인 요구 ?
def delete(req, user_id):
    target_user = get_object_or_404(User, id=user_id)
    user = req.user

    if target_user == user:
        user.delete()

    return redirect('posts:index')


@login_required
def update(req):
    if req.method == 'POST':
        form = CustomUserChangeForm(req.POST, instance=req.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:mypage')
    else:
        form = CustomUserChangeForm(instance=req.user)

    return render(req, 'accounts/form.html', {'form': form})


def password(req):
    if req.method == "POST":
        form = PasswordChangeForm(req.user, req.POST)
        if form.is_valid():
            user = form.save()
            # 비밀번호가 변경되면 자동으로 로그아웃된다.
            update_session_auth_hash(req, user)  # 자동 로그아웃을 방지
            return redirect('accounts:mypage')
    else:
        form = PasswordChangeForm(req.user)

    return render(req, 'accounts/form.html', {'form': form})


def user_page(req, user_id):
    search_user = get_object_or_404(User, id=user_id)

    # 본인은 마이페이지로.
    if req.user == search_user:
        return redirect('accounts:mypage')

    return render(req, 'accounts/user_page.html', {'search_user': search_user})


@login_required
def follow(req, user_id):
    target_user = get_object_or_404(User, id=user_id)
    user = req.user

    if target_user != user:
        if target_user in user.followings.all():
            user.followings.remove(target_user)
        else:
            user.followings.add(target_user)

    return redirect('accounts:user_page', user_id)
