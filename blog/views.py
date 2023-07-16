from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from shop.models import Product
import sys


def index(request):
    page = request.GET.get("page", "1")  # 기본 페이지 1, ?page=1
    kw = request.GET.get("kw", "")  # 검색어
    so = request.GET.get("so", "recent")  # 정렬기준
    # print('kw=' + kw, file=sys.stdout)

    if so == "recommend":  # 정렬
        post_list = Post.objects.annotate(num_voter=Count("voter")).order_by(
            "-num_voter", "-created"
        )
    else:  # recent
        post_list = Post.objects.order_by("-created")

    if kw:  # 검색
        post_list = post_list.filter(
            Q(title__icontains=kw)
            | Q(body__icontains=kw)  # 제목검색
            | Q(author__username__icontains=kw)  # 내용검색  # 작성자검색
        ).distinct()

    paginator = Paginator(post_list, 7)  # 페이지당 7개 표시
    page_object = paginator.get_page(page)

    products = Product.objects.order_by("name")
    if kw:  # 검색
        products = products.filter(
            Q(name__icontains=kw) | Q(description__icontains=kw)  # 제목검색  # 내용검색
        ).distinct()
    else:
        products = None

    return render(
        request,
        "blog/post_list.html",
        {
            "post_list": page_object,
            "page": page,
            "kw": kw,
            "so": so,
            "products": products,
        },
    )


def detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(
        request, "blog/post_detail.html", {"post": post, "product": post.product}
    )


@login_required(login_url="common:login")
def post_create(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # post 작성자 id 추가
            post.save()
            return redirect("blog:index")
    else:
        form = PostForm()
    return render(request, "blog/post_form.html", {"form": form, "product": product})


@login_required(login_url="common:login")
def post_modify(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    product = get_object_or_404(Product, id=post.product.id)
    # print(post, file=sys.stdout)

    if request.user != post.author:
        messages.error(request, "수정권한이 없습니다.")
        return redirect("blog:detail", post_id=post.id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.updated = timezone.now()  # 수정일시
            post.save()
            return redirect("blog:detail", post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, "blog/post_form.html", {"form": form, "product": product})


@login_required(login_url="common:login")
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        messages.error(request, "삭제권한이 없습니다")
        return redirect("blog:detail", post_id=post.id)

    post.delete()
    return redirect("blog:index")


@login_required()
@require_POST
def post_vote(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    action = request.POST.get("action")

    if request.is_ajax:
        print("Ajax action: " + action, file=sys.stdout)

    if post and action:
        try:
            if action == "vote":
                post.voter.add(request.user)  # 추천
                # request.user.voter_post.add(post)  # 위와 동일함
            else:
                post.voter.remove(request.user)  # 추천 취소
                # request.user.voter_post.remove(post)
            return JsonResponse({"status": "ok"})
        except:
            pass
    return JsonResponse({"status": "error"})


@login_required(login_url="common:login")
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect(
                "{}#comment_{}".format(
                    resolve_url("blog:detail", post_id=comment.post.id), comment.id
                )
            )  # 스크롤 처리 앵커
    else:
        form = CommentForm()
    return render(request, "blog/comment_form.html", {"form": form})


@login_required(login_url="common:login")
def comment_modify(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "댓글 수정권한이 없습니다")
        return redirect("blog:detail", post_id=comment.post.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.updated = timezone.now()
            comment.save()
            return redirect(
                "{}#comment_{}".format(
                    resolve_url("blog:detail", post_id=comment.post.id), comment.id
                )
            )
    else:
        form = CommentForm(instance=comment)
    return render(request, "blog/comment_form.html", {"form": form})


@login_required(login_url="common:login")
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "댓글 삭제권한이 없습니다")
        return redirect("blog:detail", post_id=comment.post_id)
    else:
        comment.delete()
    return redirect("blog:detail", post_id=comment.post_id)
