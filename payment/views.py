import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import Order
from .tasks import payment_completed
import sys

#328,358 instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.0f}',
            'payment_method_nonce': nonce,
            'options': { 'submit_for_settlement': True }
        })
        if result.is_success:
            order.paid = True   # mark the order as paid
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            
            payment_completed(order.id)     # send e-mail
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # generate token, eyJ2ZXJzaW9uIjoyLCJhdXRob3JpemF0aW9uRml.....
        client_token = gateway.client_token.generate()

        #print('client_token: ' + client_token, file=sys.stdout)
        return render(request, 'payment/process.html',
                      {'order': order, 'client_token': client_token})


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
