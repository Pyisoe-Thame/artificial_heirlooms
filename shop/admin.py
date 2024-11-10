# from django.contrib.admin.sites import AlreadyRegistered
from django.contrib import admin
from django.urls import path
from .views import sales_statistics, sales_chart, get_sales_data
from .models import Product, Category, Order, OrderItem, ShippingAddress
from django.http import HttpResponseForbidden

# import django.apps

# Register your models here.
# admin.site.register(Product)
# admin.site.register(Category)
# admin.site.register(Order)
# admin.site.register(OrderItem)
# admin.site.register(ShippingAddress)

class ShopAdminArea(admin.AdminSite):  # admin area for shop admin
    site_header = "Shop Admin Area"
    index_template = "shopadmin/index.html"

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
        extra_context.update({
            'statistics_url': 'sales_statistics',
            'chart_url': 'sales_chart',
            'data_url': 'get_sales_data'
        })
        return super().index(request, extra_context=extra_context)
    
    # Overriding the views to apply permission logic
    def sales_statistics(self, request):
        if not self.has_permission(request):
            return HttpResponseForbidden("You do not have access to this area.")
        return sales_statistics(request)

    def sales_chart(self, request):
        if not self.has_permission(request):
            return HttpResponseForbidden("You do not have access to this area.")
        return sales_chart(request)

    def get_sales_data(self, request, interval):
        if not self.has_permission(request):
            return HttpResponseForbidden("You do not have access to this area.")
        return get_sales_data(request, interval)
    
    def has_permission(self, request):
        # Only allow access if the user is authenticated and belongs to the 'Shop Admin' group
        return request.user.is_authenticated and request.user.groups.filter(name='Shop Admin').exists()

shop_site = ShopAdminArea(name="shop_admin")  # the namespace for path

shop_site.register(Product)
shop_site.register(Category)

# a shop admin should be allowed to register the following manually?
shop_site.register(Order)
shop_site.register(OrderItem)
shop_site.register(ShippingAddress)

# models = django.apps.apps.get_models()

# for model in models:

#     # Skip all models from the 'social_django' app (google acc etc.)
#     if model._meta.app_label == 'social_django':
#         continue
#     try:
#         admin.site.register(model)
#     except AlreadyRegistered:
#         pass  # skip the already register ones (the default ones)

