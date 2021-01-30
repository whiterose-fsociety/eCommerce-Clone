import json
from .models import *


def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print("Cart: ", cart)
    items = []
    order = {"get_cart_total": 0, "get_cart_items": 0, 'shipping': False}
    cartItems = order['get_cart_items']
    cartItems += sum([cart[item]['quantity'] for item in cart])
    for item in cart:
        try:
            product = Product.objects.get(id=item)
            total = (product.price * cart[item]["quantity"])

            order["get_cart_total"] += total
            order["get_cart_items"] += cart[item]["quantity"]

            order_item = {
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "imageURL": product.imageURL
                },
                "quantity": cart[item]['quantity'],
                "get_total": total,
            }
            items.append(order_item)
            print(product)
            if product.digital == False:
                order['shipping'] = True
            print(items)
        except:
            pass
    return {"cartItems": cartItems, "order": order, "items": items}


def guest_order(request, data):
    print("COOKIES: ", request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookie_cart(request)
    items = cookieData['items']
    print(items)
    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()
    order = Order.objects.create(
        customer=customer,
        complete=False
    )
    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        order_item = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer, order
