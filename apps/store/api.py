import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings

#Installed dependencies 
import stripe

#Importing Cart class
from apps.cart.cart import Cart
from .models import Product
from apps.order.models import Order

#for 'api_checkout'
from apps.order.utils import checkout
from apps.coupon.models import Coupon

def api_add_to_cart(request):

    #'json.loads()' converts JSON object into python dictionary
    #'json.dumps()' converts python dictionary into JSON object
    #'request.body' contains JSON object passed through request
    data = json.loads(request.body)

    jsonresponse = {'success':True}
    
    product_id = data['product_id']
    update = data['update']
    quantity = data['quantity']

    print(request.body)

    print(data)
    print(data['product_id'])

    #Make an instance of cart class and pass 'request'
    cart = Cart(request) 
    product = get_object_or_404(Product, pk=product_id)

    if not update:
        cart.add(product=product, quantity=1, update_quantity=False)
    else:
        cart.add(product=product, quantity=quantity, update_quantity=True)

    return JsonResponse(jsonresponse)


def api_remove_from_cart(request):

    data = json.loads(request.body)
    jsonresponse = {'success':True} 
    product_id = str(data['product_id'])

    cart = Cart(request)
    cart.remove(product_id)

    return JsonResponse(jsonresponse)



# 1st function for stripe integration
def api_create_checkout_session(request):
    data = json.loads(request.body)

    #Coupon stuff
    coupon_code = data['coupon_code']
    coupon_value = 0

    if coupon_code:
        coupon = Coupon.objects.get(code=coupon_code)
        if coupon.can_use():
            coupon_value = coupon.value
            coupon.use()


    cart = Cart(request)

    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN

    items = []

    for item in cart:
        product = item['product']

        price = int(product.price * 100)
        if coupon_value > 0:
            price = price * int(coupon_value)/100 

        obj = { 'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': product.title},
                    #need to convert unit amount to 'cents' before sending it to stripe
                    'unit_amount': int(price)
                    },
                    'quantity': item['quantity']
                }

        items.append(obj)


    session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items = items,
        mode = 'payment',
        success_url = 'http://127.0.0.1:8000/cart/success/',
        cancel_url = 'http://127.0.0.1:8000/cart/'
        )

    #Create Order
    jsonresponse = {'success':True}

    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    address = data['address']
    zipcode = data['zipcode']
    place = data['place']
    payment_intent = session.payment_intent

    orderid = checkout(request, first_name, last_name, email, address,
                      zipcode, place)

    #because 'cart.get_total_price()' was not working
    total_price = 0.00
    for item in cart:
        product = item['product']
        total_price = total_price + (float(product.price) * int(item['quantity']))
    
    if coupon_value > 0:
        total_price = total_price * int(coupon_value/100)

    order = Order.objects.get(pk=orderid)
    order.payment_intent = payment_intent
    order.paid_amount = total_price #cart.get_total_price()
    order.used_coupon = coupon_code
    order.save()


    return JsonResponse({'id':session.id})