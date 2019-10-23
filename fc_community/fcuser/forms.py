from django import forms
from .models import Fcuser
from django.contrib.auth.hashers import check_password
class LoginForm(forms.Form):
    username = forms.CharField(max_length=32, label="사용자 이름",
                               error_messages={
                                   'required': '아이디를 입력해주세요'
                               })
    password = forms.CharField(widget=forms.PasswordInput, label="비밀번호",
                               error_messages={
                                   'required': '비밀번호를 입력해주세요'
                               })

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            fcuser = Fcuser.objects.get(username=username)
            if not check_password(password, fcuser.password):
                self.add_error('password', '비밀번호가 틀렸습니다') # 특정 필드에 에러를 넣는 함수. Form 이 가지고 있음
            else:
                self.user_id = fcuser.id
