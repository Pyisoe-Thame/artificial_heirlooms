from django.urls import path
from accounts import views 
from shop import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='main/', permanent=True)),
    path('main/', views.main, name = 'main'),
    path('products/', views.products, name = 'products'),
    path('products/category/<int:category_id>/', views.products_by_category, name='products_by_category'),
    path('search/', views.search_products, name='search_products'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),  # URL for item details
    path('cart/', views.cart, name = 'cart'),
    path('update_item/', views.update_item, name = 'update_item'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('process_order/', views.processOrder, name = 'process_order')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

