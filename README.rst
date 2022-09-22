==========
Inventory 
==========

Inventory is a Django app to perform full Ecommerce inventory functionality. You get to add product specific to a category, attribute, type and brand.

For better understanding of the project, kindly check out django-htmx and mptt documentation.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "inventory" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'inventory',
        'django_htmx',
        'mptt',
    ]
    
    MIDDLEWARE = [
        ...
        'django_htmx.middleware.HtmxMiddleware',
    ]

2. Include the inventory URLconf in your project urls.py like this::

    path('', include("inventory.urls", namespace="inventory")),
OR::
    path('inventory/', include("inventory.urls", namespace="inventory")),
   

3. Run ``python manage.py migrate`` to create the inventory models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create an inventory and for better understanding of the models structure (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/inventory/ to participate in the inventory.
