from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("<slug:category_slug>/", views.product_list, name="product_list_by_category"),
    path("<int:id>/<slug:slug>/", views.product_detail, name="product_detail"),
    path("customer/profile/", views.profile, name="customer_profile"),
    path(
        "customer/profile/create/", views.profile_create, name="customer_profile_create"
    ),
    path("customer/ordered_list/", views.ordered_list, name="customer_ordered_list"),
    path("product/like/<int:product_id>", views.product_like, name="product_like"),
]
