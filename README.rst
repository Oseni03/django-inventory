==========
Inventory 
==========

Inventory is a Django app to perform full Ecommerce inventory functionality. For each question,
you get to add product specific to a category, attribute, type and brand.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "inventory" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'inventory',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('', include("inventory.urls", namespace="inventory")),
       OR 
    path('inventory/', include("inventory.urls", namespace="inventory")),
   

3. Run ``python manage.py migrate`` to create the inventory models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a inventory (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/inventory/ to participate in the inventory.