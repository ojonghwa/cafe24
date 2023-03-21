from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator
from .models import Category, Product, Like, Profile
from .forms import LikeForm, ProfileForm
from . import recommender
from blog.models import Post
from orders.models import Order, OrderItem
from django.views.decorators.http import require_POST
import sys
from django.db.models import Avg, Count


@login_required(login_url="common:login")
def log(request):
    print(request.user.username + " login", file=sys.stdout)
    return redirect("index")


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()

    page = request.GET.get("page", "1")  # 기본 페이지 1, ?page=1
    products = Product.objects.filter(available=True).order_by("-created")

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    paginator = Paginator(products, 15)  # 페이지당 15개
    page_object = paginator.get_page(page)

    return render(
        request,
        "shop/product/list.html",
        {"category": category, "categories": categories, "products": page_object},
    )


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    like_form = LikeForm()

    recommended_products = recommender.get_recommendations(id, 5)
    # print(recommended_products, file=sys.stdout)
    page = request.GET.get("page", "1")  # 기본 페이지 1, ?page=1

    post_list = Post.objects.filter(product=id).order_by("-created")
    paginator = Paginator(post_list, 5)  # 페이지당 5개
    page_object = paginator.get_page(page)

    if request.user.is_authenticated:
        like_product = Like.objects.filter(
            user=request.user, product=product
        ).values_list("grade")
        if like_product.exists():
            grade = like_product[0][0]
        else:
            grade = 0

        # product.likers.all()
        # user.like_products.all()

        # print(product.likers.all(), file=sys.stdout)   #<QuerySet [<User: admin>, <User: ojonghwa>]>
        # print(request.user.like_products.all(), file=sys.stdout)   #<QuerySet [<Product: 이한영의 Django(장고) 입문>]>

    else:
        grade = 0

    all_grade = Like.objects.filter(product=product).aggregate(
        Avg("grade"), Count("grade")
    )
    # print("all_grade: " + str(all_grade), file=sys.stdout)

    # 여기에 계산된 평점을 product.grade에 저장,  product 모델 grade 필드 추가

    return render(
        request,
        "shop/product/detail.html",
        {
            "product": product,
            "grade": grade,
            "all_grade": all_grade,
            "like_form": like_form,
            "post_list": page_object,
            "cart_product_form": cart_product_form,
            "recommended_products": recommended_products,
        },
    )


@login_required()
def profile_create(request):
    if request.method == "POST":
        profile = Profile.objects.filter(user=request.user)
        form = ProfileForm(request.POST)  # 신규 등록시

        for p in profile:  # 기존에 있을 경우 프로필정보 수정
            if p:
                form = ProfileForm(request.POST, instance=p)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.email = request.user.email
            profile.save()
        return redirect("shop:customer_profile")

    else:
        profile = []
        form = ProfileForm()
        profile = Profile.objects.filter(user=request.user)
        print("profile: " + str(profile), file=sys.stdout)
    return render(
        request, "shop/customer/profile_form.html", {"form": form, "profile": profile}
    )


@login_required()
def profile(request):
    page = request.GET.get("page", "1")  # 기본 페이지 1, ?page=1
    post_list = request.user.author_post.all()
    paginator = Paginator(post_list, 5)  # 페이지당 5개
    page_object = paginator.get_page(page)
    return render(request, "shop/customer/profile.html", {"post_list": page_object})


@login_required()
def ordered_list(request):
    page = request.GET.get("page", "1")  # 기본 페이지 1, ?page=1
    order_list = Order.objects.filter(
        user=request.user.username, paid=True
    ).all()  # 비용 지급한 목록만

    order_items = OrderItem.objects.filter(order__in=order_list)
    # print("order_items: " + str(order_items), file=sys.stdout)

    paginator = Paginator(order_list, 8)  # 페이지당 8개
    page_object = paginator.get_page(page)
    return render(
        request,
        "shop/customer/ordered.html",
        {"order_list": page_object, "order_items": order_items},
    )


# @require_POST
def product_like(request, product_id):
    if request.method == "GET":
        return JsonResponse({"error": "Request isn't POST."}, status=400)

    product = get_object_or_404(Product, id=product_id)

    # print("form.product: " + str( request.POST['product'] ), file=sys.stdout)
    # print("form.user: " + str( request.POST['user'] ), file=sys.stdout)
    print("Ajax form.grade: " + str(request.POST["grade"]), file=sys.stdout)

    # like_product = Like.objects.filter(user=request.user, product=product).values_list('grade')
    # print( like_product[0][0] , file=sys.stdout)

    # AJAX version
    if request.user.is_authenticated:
        like_product = Like.objects.filter(user=request.user, product=product)
    else:
        return JsonResponse({"error": "You aren't authenticated"}, status=400)

    if like_product.exists():
        for like in like_product:
            like.grade = int(request.POST["grade"])
            like.save()
    else:
        Like.objects.create(
            user=request.user, product=product, grade=int(request.POST["grade"])
        )

    all_grade = Like.objects.filter(product=product).aggregate(
        Avg("grade"), Count("grade")
    )
    # print( all_grade , file=sys.stdout)
    # {'grade__avg': 4.0, 'grade__count': 3}

    return JsonResponse(all_grade, status=200)
