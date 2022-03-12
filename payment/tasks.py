from io import BytesIO
#from celery import task    # launch asynchronous task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order

#356
#@task
def payment_completed(order_id):
    #Task to send an e-mail notification when an order is successfully created.
    order = Order.objects.get(id=order_id)

    # create invoice e-mail
    subject = f'Book Cafe - 주문 결재내역 no. {order.id}'
    message = '최근 구매하신 내역이 첨부되어 있으니 확인바랍니다.'
    email = EmailMessage(subject, message, 'ojonghwa@gmail.com', [order.email])

    # generate PDF, 라즈베리파이에서 사용 불가 
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets=[weasyprint.CSS(str(settings.BASE_DIR) + '/static/css/pdf.css')]

    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    # attach PDF file
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
    
    email.send()
