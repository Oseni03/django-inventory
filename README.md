# django-inventory

Django-inventory is a Django app to perform full Ecommerce inventory functionality. You get to add product specific to a category, attribute, type and brand.

For better understanding of the project, kindly check out django-htmx and mptt documentation.

Detailed documentation is in the "docs" directory.

## Quick start


1) Add "inventory" to your INSTALLED_APPS setting like this

        INSTALLED_APPS = [
            ...
            'inventory',
            'django_htmx',
            'mptt',
        ]
    
    AND

        MIDDLEWARE = [
            ...
            'django_htmx.middleware.HtmxMiddleware',
        ]

2) Include the inventory context processor to you templates option settings like this:

        TEMPLATES = [{
          ...
          'OPTIONS': {
            'context_processors': {
              ...
              'inventory.context_processors.inventory',
            }
          }
        }]
    
    to access the global context of "attributes" and "values".

3) Include the inventory URLconf in your project urls.py like this

        path('', include("inventory.urls", namespace="inventory")),
    
    OR

        path('inventory/', include("inventory.urls", namespace="inventory")),
   

4) Run ``python manage.py migrate`` to create the inventory models.

5) Start the development server and visit http://127.0.0.1:8000/admin/
   to create an inventory and for better understanding of the models structure (you'll need the Admin app enabled).

6) Visit http://127.0.0.1:8000/inventory/ to participate in the inventory.

## Optional Settings

1) INVENTORY_HOME_HTML
  Default to "inventory/home.html" which serves as your homepage. You can override this template by adding

        INVENTORY_HOME_HTML = "your desired home html"
  
    to your settings file.
  
    The home view comes with "products" and "featured" context data which can be manipulated as desired.

2) INVENTORY_SHOP_HTML
  Default to "inventory/category.html" which serves as your shop page. You can override this template by adding 

        INVENTORY_SHOP_HTML = "your desired shop html" 
    
    to your settings file.
  
    The shop view comes with "brands", "categories", "attributes" and "products" context which serves as a paginator also with and additional "url" context to issue a get request in the pagination section.

3) INVENTORY_SHOP_SUBHTML
  This template encloses the products forloop section.
  Default to "inventory/partials/shop-element.html" which serves as your shop page. You can override this template by adding 

        INVENTORY_SHOP_SUBHTML = "your desired shop element html" 
    
    to your settings file.
  
    implement this into your shop template by adding

        <div id="shop-element">
          {% include "inventory/partials/shop-element.html" %}
        </div>
    
    to your desired section/segment of your shop template.

4) INVENTORY_PRODUCT_HTML
  Default to "inventory/single-product.html" which serves as your product detail page. You can override this template by adding 

        INVENTORY_PRODUCT_HTML = "your desired product detail html" 
    
    to your settings file.
  