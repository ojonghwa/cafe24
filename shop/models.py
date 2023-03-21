from django.core import validators
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_list_by_category", args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(
        upload_to="products/%Y/%m/%d", blank=True
    )  # utils.py  uuid_name_upload_to(instance, filename)

    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    publication_date = models.DateField(blank=True, default=date(2021, 8, 7))
    # from datetime import date
    # book.publication_date = date(2021,8,7)
    isbn = models.CharField(max_length=20, blank=True, default="ISBN")
    publisher = models.CharField(max_length=50, blank=True, default="PUBL")
    contributors = models.CharField(max_length=100, blank=True, default="CONT")

    # 다대다관계 중개테이블 Like를 통해 별점 등의 정보를 추가하는게 가능
    likers = models.ManyToManyField(
        User, through="Like", related_name="like_products"
    )  # symmetrical=False

    # product.likers.all()
    # <QuerySet [<User: admin>, <User: ojonghwa>]>
    # user.like_products.all()
    # <QuerySet [<Product: 이한영의 Django(장고) 입문>]>

    class Meta:
        ordering = ("name",)
        index_together = (("id", "slug"),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])
        # path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    # like_grade = Like.objects.create(user=user1, product=product1, grade=5)
    # product1.likers.all()
    # user1.like_products.all()

    # if user1.like_products.filter(id=product1.id).exits():
    #   user1.like_products.remove(product1)
    # else:
    #   user1.like_products.add(product1)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 현 계정 사용자를 가져옴
    fullname = models.CharField(max_length=50, db_index=True, blank=True)
    address = models.CharField(max_length=250, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=30, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("fullname",)

    def __str__(self):
        return self.fullname

    def get_absolute_url(self):
        return reverse("shop:user_profile", args=[self.user])
