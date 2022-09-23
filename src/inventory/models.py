from django.db import models
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

import uuid

# Create your models here.
class Category(MPTTModel):
    """
        Inventory Category table
    """
    name = models.CharField(max_length=100, verbose_name=_("category name"), help_text=_("format: required max-100"),)
    slug = models.SlugField(max_length=150, verbose_name=_("category safe url"), help_text=_("format: required letters, numbers, underscore or hyphen"))
    is_active = models.BooleanField(default=True)
    
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True, verbose_name=_("parent of category"), help_text=_("format: not required"))
    
    class MPTTMeta:
        order_insertion_by = ["name"]
    
    class Meta:
        verbose_name = _("product category")
        verbose_name_plural = _("product categories")
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    """
        Inventory Product table
    """
    web_id = models.CharField(max_length=50, verbose_name=_("Product website ID"), help_text=_("format: required unique"), unique=True)
    name = models.CharField(max_length=255, verbose_name=_("product name"), help_text=_("format: required max-255"),)
    slug = models.SlugField(max_length=255, verbose_name=_("product safe url"), help_text=_("format: required letters, numbers, underscore or hyphen"))
    description = models.TextField(verbose_name=_("product description"), help_text=_("format: required"),)
    category = TreeManyToManyField(Category, related_name="products")
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("date product created"), help_text=_("format: y-m-d H:M:S"))
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("date product updated"), help_text=_("format: y-m-d H:M:S"))
    
    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("inventory:product-detail", args=[self.slug,])
    

class Attribute(models.Model):
    """
        Inventory Product attribute 
    """
    name = models.CharField(max_length=255, unique=True, verbose_name=_("product attribute name"), help_text=_("format: required max-255"))
    description = models.TextField(verbose_name=_("product attribute description"), help_text=_("format: required"))
    
    class Meta:
        verbose_name = _("product attribute")
        verbose_name_plural = _("product attributes")
    
    def __str__(self):
        return self.name


class ProductType(models.Model):
    """
        Inventory Product type
    """
    name = models.CharField(max_length=255, unique=True, verbose_name=_("product type"), help_text=_("format: required max-255"))
    type_attributes = models.ManyToManyField(Attribute, related_name="product_type", through="ProductTypeAttribute")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class Brand(models.Model):
    """
        Inventory Product brand
    """    
    name = models.CharField(max_length=255, unique=True, verbose_name=_("brand name"), help_text=_("format: required max-255"))
    
    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    """
        Product attribute values
    """    
    attribute = models.ForeignKey(Attribute, on_delete=models.PROTECT, related_name="values")
    value = models.CharField(max_length=255, verbose_name=_("product value"), help_text=_("format: required max-255"))
    
    def __str__(self):
        return f"{self.attribute.name} : {self.value}"


class Inventory(models.Model):
    """
        Product Inventory
    """
    sku = models.CharField(max_length=20, unique=True, verbose_name=_("stock keeping unit"), help_text=_("format: required max-20"))
    # sku = models.UUIDField(default=uuid uuid4, editable=False, primary_key=True)
    
    upc = models.CharField(max_length=12, unique=True, verbose_name=_("universal product code"), help_text=_("format: required max-12"))
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, related_name="inventory")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="inventory")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="inventory")
    attribute_values = models.ManyToManyField(
        AttributeValue, 
        related_name="inventory",
        through="ProductAttributeValues",)
    is_active = models.BooleanField(default=True, verbose_name=_("product visibility"), help_text=_("true: product-visible"))
    is_default = models.BooleanField(default=False, verbose_name=_("product default"), help_text=_("format: default=false, true=default product"))
    retail_price = models.DecimalField(
        max_digits=5, decimal_places=2, 
        verbose_name=_("recommended retail price"), 
        help_text=_("format: maximum price 999.99"), 
        error_messages={
            "name": {
                "max_length": _("the price must be between 0 and 999.99."),
            },
        },)
    store_price = models.DecimalField(
        max_digits=5, decimal_places=2, 
        verbose_name=_("regular store price"), 
        help_text=_("format: maximum price 999.99"), 
        error_messages={
            "name": {
                "max_length": _("the price must be between 0 and 999.99."),
            },
        },)
    sale_price = models.DecimalField(
        max_digits=5, decimal_places=2, 
        verbose_name=_("sale price"), 
        help_text=_("format: maximum price 999.99"), 
        error_messages={
            "name": {
                "max_length": _("the price must be between 0 and 999.99."),
            },
        },)
    discount_price = models.DecimalField(
        max_digits=5, decimal_places=2, 
        verbose_name=_("sale price"), 
        help_text=_("format: maximum price 999.99"), 
        blank = True,
        null = True,
        error_messages={
            "name": {
                "max_length": _("the price must be between 0 and 999.99."),
            },
        },)
    weight = models.FloatField(verbose_name=_("product weight"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("date sub-product created"), help_text=_("format: y-m-d H:M:S"))
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("date sub-product updated"), help_text=_("format: y-m-d H:M:S"))
    
    class Meta:
        verbose_name_plural = _("Inventory")
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.product.name
    
    def in_stock(self):
        if self.stock.units > 0:
            return "In stock"
        else:
            return "Out of stock"
    

class Media(models.Model):
    """
        Product Image table
    """
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="media")
    image = models.ImageField(upload_to="products/", verbose_name=_("product image"), help_text=_("format: required"))
    alt_text = models.CharField(max_length=255, verbose_name=_("alternate text"), help_text=_("format: required, max_length-255"))
    is_feature = models.BooleanField(default=False, verbose_name=_("product default image"), help_text=_("format: default=false, true=default image"))
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("date product image created"), help_text=_("format: y-m-d H:M:S"))
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("date product image updated"), help_text=_("format: y-m-d H:M:S"))
    
    class Meta:
        verbose_name = _("product image")
        verbose_name_plural = _("product images")


class Stock(models.Model):
    """
        Product Stock table
    """
    inventory = models.OneToOneField(Inventory, on_delete=models.PROTECT, related_name="stock")
    last_checked = models.DateTimeField(null=True, blank=True, editable=False, verbose_name=_("inventory stock check date"), help_text="format: blank-True, null-True")
    units = models.IntegerField(default=0, verbose_name=_("units/qty of stock"), help_text=_("format: required, default-0"))
    units_sold = models.IntegerField(default=0, verbose_name=_("units sold till date"), help_text=_("format: required, default-0"))
    # checked_by = models.ForeignKey("User", on_delete=models.PROTECT)
    
    class Meta:
        verbose_name_plural = _("Stock")


class ProductAttributeValues(models.Model):
    """
    Product attribute values link table
    """

    attributevalues = models.ForeignKey(
        AttributeValue,
        related_name="attributevaluess",
        on_delete=models.PROTECT,
    )
    productinventory = models.ForeignKey(
        Inventory,
        related_name="productattributevaluess",
        on_delete=models.PROTECT,
    )

    class Meta:
        unique_together = (("attributevalues", "productinventory"),)
    
    def __str__(self):
        return f"{self.productinventory} - {self.attributevalues}"


class ProductTypeAttribute(models.Model):
  """
    Product type attribute link table
  """
  attribute = models.ForeignKey(Attribute, related_name="attributes", on_delete=models.PROTECT)
  type = models.ForeignKey(ProductType, related_name="types", on_delete=models.RESTRICT)
  
  class Meta:
    unique_together = (("attribute", "type"))