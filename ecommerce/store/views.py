from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from .cookie_cart import *


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookie_cart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        print(cookieData)

    print(order)
    print("Cart Items", cartItems)
    products = Product.objects.all()
    context = {
        "products": products,
        "cartItems": cartItems
    }
    return render(request, "store/store.html", context)


"""
Error:
KeyError at /cart/
Cause 
- Cookie not available

Solution 
- Provide empty cart

Recall Cart Item

Two OrderItems
[{'quantity': 2}, {'quantity': 1}]



Tip & Code Key
When Populating The Items From A Dictionary
Remember to .__dict__ to find <model>.id and referencing <parent>.<model>.__dict__ 
"""


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookie_cart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        print(cookieData)
    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems
    }
    print("The Cart Items", cartItems)
    return render(request, "store/cart.html", context)


"""
Error 403 Forbidden
Cause 
- Not generating csrf token

Solution
- Exempt View from CSRF token
"""


# @csrf_exempt
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookie_cart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        print(order)

    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems
    }
    return render(request, "store/checkout.html", context)


def update_item(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    print("Action:", action)
    print("productID:", productID)

    customer = request.user.customer
    product = Product.objects.get(id=productID)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity += 1
    elif action == "remove":
        orderItem.quantity -= 1
    print(orderItem.quantity)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    print(orderItem.quantity)

    print(product)

    return JsonResponse("Item added", safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guest_order(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
        print("Transaction Saved...")
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            state=data['shipping']['state'],
            city=data['shipping']['city'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse("Payment Complete", safe=False)
