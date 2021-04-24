from django.db import models
from apps.store.models import Product


class Order(models.Model):
    status_choices = (
        ('ordered', 'Ordered'),
        ('shipped', 'Shipped'),
        ('arrived', 'Arrived')
        )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    zipcode = models.CharField(max_length=100)
    place = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)
    paid_amount = models.FloatField(blank=True, null=True)
    payment_intent = models.CharField(max_length=200)
    used_coupon = models.CharField(max_length=50, blank=True, null=True)
    shipped_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=status_choices,
                              default='ordered')

    def __str__(self):
        return f'{self.first_name}'


class OrderItem(models.Model):
    """ For storing the every individual 'ordered' product in the final order 
    and also its price and quantity """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.DO_NOTHING)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.id}'