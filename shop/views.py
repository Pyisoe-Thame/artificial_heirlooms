from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
import datetime
from django.db.models import Sum
from .models import *

def products(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']  # which is zero here

    products = Product.objects.all()
    categories = Category.objects.all()
    context = { 
        'products': products,
        'categories': categories,
        'cartItems': cartItems,
        'order': order,
    }
    return render(request, 'products.html', context)  # load the item_list as context

def products_by_category(request, category_id):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']  # which is zero here

    category = get_object_or_404(Category, id=category_id)

    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    context = {
        'category': category,
        'products': products,
        'categories': categories,
        'cartItems': cartItems,
        'order': order,
    }
    
    return render(request, 'products.html', context)

def search_products(request):
    query = request.GET.get('q', '')  # 'q' is the name of the search input field
    products = Product.objects.filter(name__icontains=query) if query else Product.objects.all()
    categories = Category.objects.all()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']  # which is zero here
    
    context = { 
        'products': products, 
        'caegories': categories,
        'query': query,
        'order': order,
    }

    return render(request, 'products.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Retrieve the item based on ID
    categories = Category.objects.all()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}

    context = { 
        'product': product,
        'categories': categories,
        'order': order,
    }
    return render(request, 'product_detail.html', context)  # Render the item detail template

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    
    context = { 
        'items': items,
        'order': order,
    }
    return render(request, 'cart.html', context)

def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print('product id', productId)
    print('action', action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1) 
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was updated', safe=False)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    
    context = { 
        'items': items,
        'order': order
    }
    return render(request, 'checkout.html', context)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.filter(customer=customer, complete=False).first()  # only process the existing data

        if not order:  # No matching order found
            if data['form']['total'] == 0:  # Ensure the cart total isn't empty
                return JsonResponse('Cannot create order with empty data', safe=False)
            order = Order.objects.create(customer=customer, complete=False)

        total = int(data['form']['total'])
        if total == order.get_cart_total:  # double check with total from request and total from cart.js to ensure security
            print(total)
            print(order.get_cart_total)
            order.transaction_id = transaction_id
            order.complete = True
            order.save()

        # if shipping is true
        ShippingAddress.objects.create(  # query create the shipping address
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode']
            # country can be added if the request has it
        ) 
    else:
        print('The user is not logged in.')
    return JsonResponse('Payment submitted...', safe=False)

def main(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    
    categories = Category.objects.all()
    context = { 
        'categories': categories,  # for the Products dropdown-menu
        'items': items,
        'order': order
    }
    return render(request, 'main.html', context)

