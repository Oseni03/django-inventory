from django.urls import path
from . import views


app_name = "inventory"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("shop/", views.ShopView.as_view(), name="shop"),
    path("product/<slug:slug>/", views.ProductDetailView.as_view(), name="product-detail"),
    
    
    path("category/<slug:slug>/", views.category_products, name="category-products"),
    path("brand/<int:pk>/", views.brand_products, name="brand-products"),
    path("attr/<pk>/", views.attr_products, name="attr-products"),
]