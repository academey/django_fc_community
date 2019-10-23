from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Fcuser
from django.contrib.auth.hashers import make_password, check_password
from .forms import LoginForm


def home(request):
    user_id = request.session.get('user')
    if user_id:
        fcuser = Fcuser.objects.get(pk=user_id)
        return HttpResponse(fcuser.username)
    return HttpResponse("home!")


def logout(request):
    if request.session.get('user'):
        del (request.session['user'])

        return redirect('/')


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid(): # 내재된 검증 함수
            request.session['user'] = form.user_id
            return redirect('/')
    else:
        form = LoginForm() # 빈 폼을 전달해서 뷰에 렌더링시켜ㅑ줌

    return render(request, 'login.html', {'form': form})

    # if request.method == 'GET':
    #     return render(request, 'login.html')
    # elif request.method == 'POST':
    #     username = request.POST.get('username', None)
    #     password = request.POST.get('password', None)
    #
    #     res_data = {}
    #
    #     if not (username and password):
    #         res_data['error'] = '모든 값을 입력해야 합니다.'
    #     else:
    #         fcuser = Fcuser.objects.get(username=username)
    #         if check_password(password, fcuser.password):
    #             # 비밀번호 일치 로그인 성공
    #             # TODO: 세션 처리도 해줘야 함
    #             request.session['user'] = fcuser.id
    #             return redirect('/')
    #         else:
    #             res_data['error'] = '비번 틀림'
    #     return render(request, 'login.html', res_data)


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')  # 이 파일의 경로는 templates 을 보고 있으니 거기서 있으면 연결해준다.
    if request.method == 'POST':
        username = request.POST.get('username', None)
        useremail = request.POST.get('useremail', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re-password', None)

        res_data = {}

        if not (username and useremail and password and re_password):
            res_data['error'] = '모든 값을 입력해야 합니다.'
        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다'
        else:
            fcuser = Fcuser(
                username=username,
                useremail=useremail,
                password=make_password(password)
            )
            fcuser.save()

        return render(request, 'register.html', res_data)
