from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
from django.utils import timezone


class Post(models.Model):
    STATUS_CHOICES = (
        ("draft", "비공개"),
        ("published", "공개"),
    )
    title = models.CharField(max_length=250)
    body = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_post"
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # publish = models.DateTimeField(default=timezone.now)       #admin, for date_hierarchy
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="published"
    )

    voter = models.ManyToManyField(User, related_name="voter_post")
    # 글을 추천한 모든 유저들
    # post.voter.all() = <QuerySet [<User: admin>, <User: ojonghwa>]>

    # 유저가 추천한 모든 글들 조회
    # post.author.voter_post.all() = [<QuerySet [<Post: 공부해 봅시다.>, <Post: 도킨스가 칭찬할 만하다>,
    # request.user.voter_post.all()

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ("created",)
