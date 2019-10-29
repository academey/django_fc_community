from django.shortcuts import render
# from fc_community.fcuser.models import Fcuser
from .models import Board
from .forms import BoardForm
from fcuser.models import Fcuser
from django.shortcuts import render, redirect, Http404
from django.core.paginator import Paginator


def board_detail(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다.')

    return render(request, 'board_detail.html', {'board': board})


def board_list(request):
    all_boards = Board.objects.all().order_by('-id')  # 생성된 순서 역순으로 가지고 오겠다.
    page = int(request.GET.get('p', 1))  # string -> int
    paginator = Paginator(all_boards, 2)  # 한 페이지에 2개씩!

    boards = paginator.get_page(page)
    return render(request, 'board_list.html', {'boards': boards})


def board_write(request):
    if not request.session.get('user'):
        return redirect('/fcuser/login')
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():  # 내재된 검증 함수
            user_id = request.session.get('user')
            fcuser = Fcuser.objects.get(pk=user_id)

            board = Board()
            board.title = form.cleaned_data.get('title')
            board.contents = form.cleaned_data.get('contents')
            board.writer = fcuser
            board.save()

            return redirect('/board/list')
    else:
        form = BoardForm()  # 빈 폼을 전달해서 뷰에 렌더링시켜 줌

    return render(request, 'board_write.html', {'form': form})
