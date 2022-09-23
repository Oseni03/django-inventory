from django.contrib import admin
from .models import Stock, Media, Inventory, AttributeValue, Brand, Attribute, Product, Category, ProductAttributeValues, ProductType, ProductTypeAttribute


admin.site.register(ProductAttributeValues)
admin.site.register(Brand)

class ProductMediaInline(admin.TabularInline):
    model = Media 


class TypeAttributeInline(admin.TabularInline):
    model = ProductTypeAttribute 


class StockInline(admin.TabularInline):
    model = Stock 


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue 


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    inlines = [ProductMediaInline, StockInline]
    search_fields = ['product']
    list_display = ('__str__', 'product_type', 'product', "brand", "sale_price")
    list_filter = (
      ('brand', admin.RelatedOnlyFieldListFilter),
      ('product_type', admin.RelatedOnlyFieldListFilter),
      ("is_active", admin.BooleanFieldListFilter), 
      ("is_default", admin.BooleanFieldListFilter), 
    )
    list_select_related = ('product_type', 'product', "brand")
    list_per_page = 50


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    inlines = [
        AttributeValueInline
    ]


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        TypeAttributeInline
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("name",),
    }
    list_per_page = 50


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("name",),
    }
    list_filter = (
      ('category', admin.RelatedOnlyFieldListFilter),
      ("is_active", admin.BooleanFieldListFilter), 
      ("is_featured", admin.BooleanFieldListFilter), 
      ("is_bestseller", admin.BooleanFieldListFilter), 
    )
    list_per_page = 50