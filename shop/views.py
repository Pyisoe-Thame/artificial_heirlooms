from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.db import transaction  # to prevent race condition

from .models import *

def products(request):

    if request.user.is_authenticated:
        customer = request.user
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
        customer = request.user
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
        customer = request.user
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
        customer = request.user
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
        customer = request.user
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

    customer = request.user
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        if orderItem.quantity >= product.stock:  # cannot demand more than supply
            return JsonResponse('Item count cannot exceed the product stock.', safe=False)
        orderItem.quantity = (orderItem.quantity + 1) 
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was updated', safe=False)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
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
    transaction_id = timezone.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user
        order = Order.objects.filter(customer=customer, complete=False).first()  # only process the existing data

        if not order:  # No matching order found
            if data['form']['total'] == 0:  # Ensure the cart total isn't empty
                return JsonResponse('Cannot create order with empty data', safe=False)
            order = Order.objects.create(customer=customer, complete=False)

        total = int(data['form']['total'])
        if total == order.get_cart_total:  # double check with total from request and total from cart.js to ensure security
            
            order.transaction_id = transaction_id
            order.complete = True
            order.date_ordered = timezone.now()  # set the order completion time
            
            with transaction.atomic():  # this acts like a lock
                order.save()

                # reduce stock for each item in the order
                order_items = order.orderitem_set.all()  # get all OrderItems for the order
                for item in order_items:
                    
                    # lock this product row to prevent other transactions from modifying it
                    product = Product.objects.select_for_update().get(id=item.product.id)
                    product.stock -= item.quantity  # reduce stock 
                    product.stock = max(product.stock, 0)  # ensure stock does not go below zero
                    product.save()

                    # update other incomplete orders for the same product
                    other_order_items = OrderItem.objects.filter(order__complete=False, product=product)
                    for other_order_item in other_order_items:
                        if product.stock == 0:
                            other_order_item.delete()  # remove if out of stock
                        elif other_order_item.quantity > product.stock:
                            other_order_item.quantity = product.stock  # set to available stock amount
                            other_order_item.save()

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

def thankyou(request):
    if request.user.is_authenticated:
        customer = request.user
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

    return render(request, 'thankyou.html', context)

def main(request):
    if request.user.is_authenticated:
        customer = request.user
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

def sales_statistics(request):
    # Get the current time
    now = timezone.now()

    # Calculate sales within the day, month, and year
    daily_sales = OrderItem.objects.filter(date_added__date=now.date()).aggregate(
        total_items_sold=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('product__price'))
    )
    
    monthly_sales = OrderItem.objects.filter(date_added__year=now.year, date_added__month=now.month).aggregate(
        total_items_sold=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('product__price'))
    )
    
    yearly_sales = OrderItem.objects.filter(date_added__year=now.year).aggregate(
        total_items_sold=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('product__price'))
    )

    context = {
        'daily_sales': daily_sales,
        'monthly_sales': monthly_sales,
        'yearly_sales': yearly_sales,
    }

    return render(request, 'shopadmin/sales_statistics.html', context)

def sales_chart(request):
    return render(request, 'shopadmin/sales_chart.html')

def get_sales_data(request, interval):
    # initial query for completed orders
    orders = Order.objects.filter(complete=True)

    # initialize labels, sales_data, and order_counts lists
    labels = []
    sales_data = []
    order_count = []
    
    # Filter based on the interval
    if interval == 'week':
        start_date = timezone.now() - timedelta(days=7)
        orders = orders.filter(date_ordered__gte=start_date)

        # aggregate sales data by day in the last 7 days
        for day in range(7):
            date = timezone.now() - timedelta(days=day)
            daily_orders = orders.filter(date_ordered__date=date.date())
            day_sales = sum(order.get_cart_total for order in daily_orders)
            day_orders = daily_orders.count()

            # store both human-readable and sortable date
            human_readable_date = date.strftime('%b. %d, %Y')  # e.g., 'Nov. 10, 2024'
            sortable_date = date.strftime('%Y-%m-%d')  # e.g., '2024-11-10'
    
            labels.append({'label': human_readable_date, 'sortable': sortable_date})
            sales_data.append(day_sales)
            order_count.append(day_orders)

    elif interval == 'month':
        start_date = timezone.now() - timedelta(days=30)
        orders = orders.filter(date_ordered__gte=start_date)

        # aggregate sales data by day in the last month
        for day in range(30):
            date = timezone.now() - timedelta(days=day)
            daily_orders = orders.filter(date_ordered__date=date.date())
            day_sales = sum(order.get_cart_total for order in daily_orders)
            day_orders = daily_orders.count()

            # store both human-readable and sortable date
            human_readable_date = date.strftime('%b. %d')  # e.g., 'Nov. 10'
            sortable_date = date.strftime('%Y-%m-%d')  # e.g., '2024-11-10'
    
            labels.append({'label': human_readable_date, 'sortable': sortable_date})
            sales_data.append(day_sales)
            order_count.append(day_orders)

    elif interval == 'year':
        start_date = timezone.now() - timedelta(days=365)
        orders = orders.filter(date_ordered__gte=start_date)

        # Aggregate sales data by month in the last year
        for month in range(12):
            date = timezone.now() - timedelta(days=30 * month)
            monthly_orders = orders.filter(date_ordered__year=date.year, date_ordered__month=date.month)
            month_sales = sum(order.get_cart_total for order in monthly_orders)
            month_orders = monthly_orders.count()

            # store both human-readable and sortable date
            human_readable_date = date.strftime('%Y %b.')  # e.g., 'Nov. 2024'
            sortable_date = date.strftime('%Y-%m-%d')  # e.g., '2024-11-10'
    
            labels.append({'label': human_readable_date, 'sortable': sortable_date})
            sales_data.append(month_sales if month_sales else 0)
            order_count.append(month_orders)

    else:
        return JsonResponse({'error': 'Invalid interval'}, status=400)
    
    return JsonResponse({'labels': labels, 'sales_data': sales_data, 'order_count': order_count})

