from django.shortcuts import render, get_object_or_404

from .models import Item

def items(request):
    item_list = Item.objects.all()
    context = {
        'item_list': item_list
    }
    return render(request, 'items.html', context)  # load the item_list as context

def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)  # Retrieve the item based on ID
    return render(request, 'item_detail.html', {'item': item})  # Render the item detail template

def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'checkout.html')

def main(request):
    return render(request, 'main.html')

