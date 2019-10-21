from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
# Create your views here.


def index(req):
    return render(req, 'accounts/index.html')


def signup(req):
    if req.user.is_authenticated:
        return redirect('accounts:index')

    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            user = form.save()
            auth_login(req, user)
            return redirect('accounts:index')
    else:
        form = UserCreationForm()
    return render(req, 'accounts/form.html', {'form': form})


def login(req):
    if req.user.is_authenticated:
        return redirect('accounts:index')

    if req.method == "POST":  # 인증만 하는 것이기 때문에 form.get_user로 유저 정보를 가져와야함
        form = AuthenticationForm(req, req.POST)
        if form.is_valid():
            auth_login(req, form.get_user())
            return redirect(req.GET.get('next') or 'accounts:index')
    else:
        form = AuthenticationForm()

    return render(req, 'accounts/form.html', {'form': form})


def logout(req):
    auth_logout(req)
    return redirect('accounts:index')
