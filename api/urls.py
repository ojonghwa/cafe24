from rest_framework import routers
from django.urls import path, include
from . import views

app_name = "shop_api"

router = routers.DefaultRouter()

# http://127.0.0.1:8000/api/category/",
# http://127.0.0.1:8000/api/category/1/",

router.register("category", views.CategoryViewSet)
router.register("product", views.ProductViewSet)
router.register("post", views.PostViewSet)
router.register("user", views.UserViewSet)
router.register("order", views.OrderViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("login/", views.Login.as_view(), name="login"),
    # path('category/', views.CategoryListView.as_view(), name='category_list'),
    # path('category/<pk>/', views.CategoryProductView.as_view(), name='product_list'),
    # path('product/<pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    # path('order/<pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path(
        "orderitem/<pk>/", views.OrderItemDetailView.as_view(), name="orderitem_detail"
    ),
    path(
        "orderlist/<username>/", views.OrderListDetailView.as_view(), name="order_list"
    ),
    path("iot/", views.iot_esp8266View.as_view()),
    path("getDustData/", views.getDustData.as_view()),
    path("getCoronaData/", views.getCoronaData.as_view()),
    path("getWeatherData/<city>/", views.getWeatherData.as_view()),
]
