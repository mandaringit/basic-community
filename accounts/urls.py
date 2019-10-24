from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('profile/', views.mypage, name='mypage'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:user_id>/', views.user_page, name="user_page"),
    path('<int:user_id>/follow/', views.follow, name="follow"),
    path('<int:user_id>/delete/', views.delete, name="delete"),
    path('udpate/', views.update, name="update"),
    path('password/', views.password, name='password'),
]
