from django.contrib.admin.sites import AlreadyRegistered
from django.contrib import admin
from django.urls import path
from .views import sales_statistics, sales_chart, get_sales_data
from .models import Product, Category, Order, OrderItem, ShippingAddress

import django.apps

# Register your models here.
# admin.site.register(Product)
# admin.site.register(Category)
# admin.site.register(Order)
# admin.site.register(OrderItem)
# admin.site.register(ShippingAddress)

class ShopAdminArea(admin.AdminSite):
    site_header = "Shop Admin Area"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sales-statistics/', self.admin_view(sales_statistics), name='sales_statistics'),
            path('sales-chart/', self.admin_view(sales_chart), name='sales_chart'),
            path('get-sales-data/<str:interval>/', self.admin_view(get_sales_data), name='get_sales_data'),
        ]
        return custom_urls + urls
    
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['statistics_url'] = 'sales_statistics'  # Pass the URL name for use in the template
        return super().index(request, extra_context=extra_context)

shop_site = ShopAdminArea(name="Shop Admin")

shop_site.register(Product)
shop_site.register(Category)

# a shop admin should be allowed to register the following manually?
# shop_site.register(Order)
# shop_site.register(OrderItem)
# shop_site.register(ShippingAddress)

# models = django.apps.apps.get_models()

# for model in models:

#     # Skip all models from the 'social_django' app (google acc etc.)
#     if model._meta.app_label == 'social_django':
#         continue
#     try:
#         admin.site.register(model)
#     except AlreadyRegistered:
#         pass  # skip the already register ones (the default ones)

