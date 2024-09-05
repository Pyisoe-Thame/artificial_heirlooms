from django.urls import path
from accounts import views 
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='main/', permanent=True)),
    path('main/', views.main, name = 'main'),
    path('items/', views.items, name = 'items'),
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),  # URL for item details
    path('cart/', views.cart, name = 'cart'),
    path('checkout/', views.checkout, name = 'checkout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

