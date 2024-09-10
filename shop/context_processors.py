from django.db.models import Sum
from .models import OrderItem

def cart_item_count(request):
    if request.user.is_authenticated:
        order_items = OrderItem.objects.filter(order__customer=request.user.customer).aggregate(total_items=Sum('quantity'))
        return {'cart_item_count': order_items['total_items'] or 0}
    return {'cart_item_count': 0}

