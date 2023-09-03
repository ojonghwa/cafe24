from .cart import Cart

def cart(request):      #302
    return {'cart': Cart(request)}
