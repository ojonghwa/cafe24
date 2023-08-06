from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include
from .views import MyTokenObtainPairView
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
    path("signup/", views.Signup.as_view(), name="signup"),
    # JWT 인증
    path("token/", MyTokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
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
