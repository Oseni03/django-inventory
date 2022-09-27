from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.conf import settings

from .models import Product, Brand, Attribute, Category, ProductTypeAttribute, Inventory

# Create your views here.
class HomeView(generic.TemplateView):
    try:
        template_name = settings.INVENTORY_HOME_HTML
    except AttributeError:
        template_name = "inventory/home.html"
    
    def get_context_data(self):
        context = super().get_context_data()
        context["products"] = Inventory.objects.prefetch_related("product").filter(
          product__is_active=True, 
          is_default=True, 
          is_active=True)[:10]
        context["featured"] = Inventory.objects.prefetch_related("product").filter(
          product__is_featured=True, 
          product__is_active=True, 
          is_default=True, is_active=True)
        return context


class ShopView(generic.ListView):
    try:
        template_name = settings.INVENTORY_SHOP_HTML
    except AtrributeError:
        template_name = "inventory/category.html"
    context_object_name = "products"
    paginate_by = 10
    
    def get_queryset(self):
      products = Inventory.objects.prefetch_related("product").filter(product__is_active=True, is_default=True, is_active=True)
      return products
    
    def get_context_data(self):
        context = super().get_context_data()
        context["brands"] = Brand.objects.all()[:10].prefetch_related("inventory")
        context['categories'] = Category.objects.all().prefetch_related("products")
        context['attributes'] = Attribute.objects.all().prefetch_related("values__inventory")
        context["url"] = reverse("inventory:shop")
        return context 
    

def category_products(request, slug):
    products = Inventory.objects.prefetch_related("product").filter(
      product__is_active=True,
      product__category__slug=slug, 
      is_default=True, is_active=True)
    
    paginator = Paginator(products, 10) # Show 10 products per page.

    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        "products": products,
        "url": reverse("inventory:category-products", args=[slug,])
    }
    try:
        return render(request, settings.INVENTORY_SHOP_SUBHTML, context)
    except AtrributeError:
        return render(request, "inventory/partials/shop-element.html", context)


def brand_products(request, pk):
    products = Inventory.objects.prefetch_related("product", "brand").filter(
      brand__id=pk,
      product__is_active=True,
      is_default=True, is_active=True)
    
    paginator = Paginator(products, 10) # Show 10 products per page.

    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        "products": products,
        "url": reverse("inventory:brand-products", args=[pk,])
    }
    try:
        return render(request, settings.INVENTORY_SHOP_SUBHTML, context)
    except AtrributeError:
        return render(request, "inventory/partials/shop-element.html", context)


def attr_products(request, pk):
    #value = request.GET.get("attr_val")
    products = Inventory.objects.prefetch_related("product", "attribute_values").filter(
      attribute_values__id=pk,
      product__is_active=True,
      is_default=True, is_active=True)
    
    paginator = Paginator(products, 10) # Show 10 products per page.

    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        "products": products,
        "url": reverse("inventory:attr-products", args=[pk,]),
    }
    try:
        return render(request, settings.INVENTORY_SHOP_SUBHTML, context)
    except AtrributeError:
        return render(request, "inventory/partials/shop-element.html", context)


class ProductDetailView(generic.DetailView):
    model = Product 
    context_object_name = "invt"
    try:
        template_name = settings.INVENTORY_PRODUCT_HTML
    except AtrributeError:
        template_name = "inventory/single-product.html"
    
    def get_object(self, **kwargs):
      prod = super().get_object(**kwargs)
      obj = Inventory.objects.get(
          product=prod, is_default=True, 
          product__is_active=True)
      return obj
    
    def get_context_data(self, **kwargs):
      context = super().get_context_data()
      obj = self.object
      attributes = ProductTypeAttribute.objects.prefetch_related("attribute__values", "type").filter(type__inventory__product=obj.product)
      
      values = obj.attribute_values.values("value")
      
      context["attributes"] = attributes
      context["values"] = [val["value"] for val in values]
      return context