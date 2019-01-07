from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import Post
from .forms import PostForm
# get_object_or_404 : '알맞은 페이지를 띄우거나, page not found 에러 화면을 띄워라'에 해당하는 shortcut
# get_object_or_404, render, redirect는 장고가 제공해주는 템플릿 시스템

# Create your views here.
# render함수의 세 가지 인자. 마지막 인자는 비우고 인자 두 개만 써도 됨

def post_list(request):
    qs = Post.objects.all()
    qs = qs.filter(published_date__lte=timezone.now())
    qs = qs.order_by('published_date')

    return render(request, 'blog/post_list.html', {
        'post_list': qs, 
    })

def post_detail(request, pk):
    # post = Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {
        'post': post,
    })

def post_new(request):
    # 아래 처리를 안해주면 글을 작성해도 DB에 저장이 안 됨.
    # 뭔가 입력받았을 때 페이지 간 이동이 POST 방식으로 넘어간다
    # 따라서 request의 method가 POST 방식이면, 해당 데이터를 받아서 저장하겠다
    # else로 넘어가는 경우는 POST 방식이 아닐 경우 즉, GET 방식일 경우
    # GET 방식으로 넘어가는 경우는? 입력한 내용없이 '처음 페이지에 접속했을 때'
    # is_valid() : 장고는 폼의 유효성 검사를 할 수 있음
    # 그렇지만 우선 save 눌렀는데 빈칸이 있다면, '브라우저'가 해당 오류를 먼저 띄워줌
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk = post.pk)
            # 작성 잘 되었으면 해당 글의 post_detail로 이동하겠다
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {
        'form' : form,
    })

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        # 수정 폼에는 기존 데이터 채워져 있어야 하기 때문에 instance=post 추가!
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {
        'form': form
    })