from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from apps.Core_app.views import frontpage, contact, about
from apps.store.views import product_detail, category_detail
from apps.cart.views import cart_detail, success
from apps.cart.webhook import webhook

from apps.store.api import (
        api_add_to_cart, api_remove_from_cart, 
        api_create_checkout_session
        )
from apps.coupon.api import api_can_use

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', frontpage, name='frontpage'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('cart/', cart_detail, name='cart'),
    path('hooks/', webhook, name='webhook'),
    path('cart/success/', success, name='success'),

    #API
    path('api/add_to_cart', api_add_to_cart, name='api_add_to_cart'),
    path('api/remove_from_cart', api_remove_from_cart, name='api_remove_from_cart'),
    path('api/create_checkout_session', api_create_checkout_session, name='api_create_checkout_session'),
    path('api/can_use/', api_can_use, name='api_can_use'),

    #Store
    path('<slug:category_slug>/<slug:slug>/', product_detail, name='product_detail'),
    path('<slug:slug>/', category_detail, name='category_detail'),
]


#Below Url was added to server media files in dev environment from root folder
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

