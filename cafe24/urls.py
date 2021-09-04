from django.contrib import admin
from django.urls import path, include
from shop import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.product_list, name='index'),
    path('common/', include('common.urls')),
    path('log', views.log, name='log'),
    path('blog/', include('blog.urls')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    path('api/', include('api.urls', namespace='shop_api')),
]

handler404 = 'common.views.page_not_found'

# when serving media in production, url mapping and views is not set up automatically for media files. 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
