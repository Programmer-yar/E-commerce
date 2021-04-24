from django.conf import settings
from apps.store.models import Product

class Cart(object):

    def __init__(self, request):

        #loads the session dictionary from request object
        #Read Notes in Root folder for more info about sessions
        self.session = request.session 

        """gets the 'value' of 'key' inside "CART_SESSION_ID"
        from session dictionary
        - This key was defined by us in 'settings.py' 
        - By default this key contains 'None' """
        cart = self.session.get(settings.CART_SESSION_ID)

        #Runs If cart is 'empty'/'empty dictionary' or conatins 'None' 
        if not cart:
            #adds "CART_SESSION_ID" as 'key' and "{}" as 'value' to session 
            #dictionary, cart variable also stores empty dictionary
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        """ To iterate through database and find the product """

        #Stores all the keys of 'self.cart' dictionary
        product_ids = self.cart.keys()
        product_clean_ids = []

        #Suppose 'self.cart' contains dict as '{'2':{'quantity':1, 'price':110, 'id':2}}'
        #Then "product_ids" contain '2'
        for every_id in product_ids:
            product_clean_ids.append(every_id)
            #Adding new key 'product' into each self.cart 'value' with
            #object from database as 'value'
            self.cart[str(every_id)]['product'] = Product.objects.get(pk=every_id)
            #Now the 'self.cart' will become
            #'{'2':{'quantity':1, 'price':110, 'id':2, 'product': <Product: Redmi Note 8>}}'

        for item in self.cart.values():
            #Adding another key to each cart value
            item['total_price'] = float(item['price']) * int(item['quantity'])
            #Now the 'self.cart' will become
            #'{'2':{'quantity':1, 'price':110, 'id':2, 
            #  'product': <Product: Redmi Note 8>, 'total_price': 150 }}'

            #This yield is instantaneously giving output to the instance
            #in views
            yield item


    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        price = product.price

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0, 'price':price, 'id':product_id}
            
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] = self.cart[product_id]['quantity'] + 1

        self.save()

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        """Saves the cart variable in session dictionary"""
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def get_total_length(self):
        """Iterating through each cart value and adds the 'value' stored
        in 'quantity' 'key'
        Example structure: '{
        '2':{'quantity':1, 'price':110, 'id':2},
        '3':{'quantity':1, 'price':150, 'id':3}
        }' """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_cost(self):
        #make sense out of this statement
        return sum(float(item['total_price']) for item in self)


    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
