from django.shortcuts import render
from django.conf import settings
from .cart import Cart

def cart_detail(request):
    # print('*'*10, request.session.keys())
    # print('*'*10, request.session.values())
    
    # cart = request.session.get(settings.CART_SESSION_ID)
    # print('*'*10, cart)

    cart = Cart(request)

    #testing
    print('*'*10, 'The cart instance: ', cart)
    print('The cart variable', cart.cart)
    productstring = ''

    for item in cart:
        #testing
        print('when looping through cart instance', item)

        product = item['product']
        #b = f"{{ 'id': {product.id}, 'title': {product.title}, 'price': {product.price}, 'quantity': {item['quantity']}, 'total_price': {item['total_price']} }}"
        b = "{'id': '%s', 'title': '%s', 'price': '%s', 'quantity':  '%s', 'total_price': '%s' }," %(product.id, product.title, product.price, item['quantity'], item['total_price'])
        productstring = productstring + b


    context = {
            'cart':cart,
            'pub_key': settings.STRIPE_API_KEY_PUBLISHABLE,
            'productstring':productstring
        }
        
    return render(request, 'cart.html', context)

def success(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'success.html')