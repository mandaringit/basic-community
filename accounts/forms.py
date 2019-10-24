from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
# settings.AUTH_USER_MODEL => 'accounts.User' 라는 스트링을 반환한다.


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()  # User 클래스. 이름에 구애받지 않는다.
        fields = ['first_name', 'last_name', 'email']
