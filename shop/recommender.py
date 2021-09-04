from django.shortcuts import get_object_or_404
from orders.models import OrderItem
from .models import Product
from pandas import DataFrame
#import sys


def get_recommendations(id, max_results=3):
    orders_for_product = OrderItem.objects.filter(product_id=id)
    #<QuerySet [<OrderItem: 19>, <OrderItem: 22>, <OrderItem: 23>]>

    order_ids = [p.order_id for p in orders_for_product]
    #[13, 14, 15]

    order_ids = OrderItem.objects.filter(order_id__in=order_ids)
    #<QuerySet [<OrderItem: 19>, <OrderItem: 20>, <OrderItem: 21>, <OrderItem: 22>]>

    product_ids = [p.product_id for p in order_ids if p.product_id != id]
    #[11, 15, 15, 11]

    product_ids.sort()
    #[11, 11, 15, 15]
    num_orders_for_product = len(product_ids)
    #4

    product_list = []
    [product_list.append(i) for i in product_ids if i not in product_list]
    #[11, 15]

    count_list = []
    [count_list.append(product_ids.count(i)/num_orders_for_product) for i in product_list]
    #[0.5, 0.5]

    raw_data = {'product_id': product_list, 'frequency': count_list }
    dataframe = DataFrame(raw_data)
    dataframe = DataFrame(dataframe.sort_values("frequency", ascending=False).head(max_results))
    #   product_id  frequency
    #0          11        0.5
    #1          15        0.5

    recommends_ids = dataframe.product_id.tolist()
    #print(recommends_ids, file=sys.stdout)
    #[11, 15]

    product_ids = Product.objects.filter(id__in=recommends_ids)
    
    return product_ids
