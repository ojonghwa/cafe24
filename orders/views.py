import weasyprint
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm
#from .tasks import order_created
from shop.models import Profile
import sys


def order_create(request):      #376
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            if not request.user.is_authenticated:
                order.user = ''

            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()

            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'], quantity=item['quantity'])
            cart.clear()

            #launch asynchronous task
            #order_created.delay(order.id)
            #order_created(order.id)    #비동시 처리할 경우 위의 것
            
            #326, set the order in the session
            request.session['order_id'] = order.id

            #return render(request, 'orders/order/created.html', {'order': order }) 
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
        profile = []
        if request.user.is_authenticated:
            profile = Profile.objects.filter(user=request.user)
            #print("profile: " + str(profile), file=sys.stdout)

    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form, 'profile': profile })



@staff_member_required
def admin_order_detail(request, order_id):          #343, create a custom admin view 
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'

    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(str(settings.BASE_DIR) + '/static/css/pdf.css')])

    return response
    
    