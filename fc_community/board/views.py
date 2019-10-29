from django.shortcuts import render
# from fc_community.fcuser.models import Fcuser
from .models import Board
from .forms import BoardForm
from fcuser.models import Fcuser
from tag.models import Tag
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

            tags = form.cleaned_data['tags'].split(',')

            board = Board()
            board.title = form.cleaned_data.get('title')
            board.contents = form.cleaned_data.get('contents')
            board.writer = fcuser
            board.save()

            for tag in tags:
                if not tag:
                    continue
                # name = tag 조건이 일치한다면 가져오고, 맞지 않다면 생성해준다.
                # 생성되면 crated를 boolean True 로 리턴하기 때문에 고걸로 케이스를 제어할 수도 있다.
                _tag, _created = Tag.objects.get_or_create(name=tag)
                # if _created ~~ 로직 넣을수도 있다는 말임.

                # 만약 board.save 전에 add를 하면 에러가 난다. 왜냐면 board를 생성할 때 id가 만들어지는데, 그 이후에
                # m:n 관계를 연결할 수 있기 때문이다.
                board.tags.add(_tag)


            return redirect('/board/list')
    else:
        form = BoardForm()  # 빈 폼을 전달해서 뷰에 렌더링시켜 줌

    return render(request, 'board_write.html', {'form': form})
