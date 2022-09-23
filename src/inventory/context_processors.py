from .models import Product, Inventory
from django.conf import settings


def inventory(request):
    return {
       "bestsellers": Inventory.objects.prefetch_related("product").filter(
         product__is_bestseller=True, 
         product__is_active=True, 
         is_default=True, 
         is_active=True),
    }

