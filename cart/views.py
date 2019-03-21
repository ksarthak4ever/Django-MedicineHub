from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from . models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist


def _cart_id(request): #Checking if session id has been created in the customer browser
	cart = request.session.session_key
	if not cart:
		cart = request.session.create() #if no session id then create one for the cart
	return cart


def add_cart(request, product_id): #view for adding products to cart
	product = Product.objects.get(id=product_id)
	try:
		cart = Cart.objects.get(cart_id= _cart_id(request))
	except Cart.DoesNotExist:
		cart = Cart.objects.create(
				cart_id = _cart_id(request)
			)
		cart.save()
	try:
		cart_item = CartItem.objects.get(product=product, cart=cart)
		if cart_item.quantity < cart_item.product.stock: #checking if products added in cart are not more than the stock of the product
			cart_item.quantity += 1
		cart_item.save()
	except CartItem.DoesNotExist:
		cart_item = CartItem.objects.create(
				product = product,
				quantity = 1,
				cart = cart
			)
		cart_item.save()
	return redirect('cart:cart_detail')


def cart_detail(request, total=0, counter=0, cart_items = None): #View for cart detail 
	try:
		cart = Cart.objects.get(cart_id = _cart_id(request))
		cart_items = CartItem.objects.filter(cart=cart, active=True)
		for cart_item in cart_items:
			total += (cart_item.product.price * cart_item.quantity)
			counter	+= cart_item.quantity
	except ObjectDoesNotExist:
		pass

	return render(request, 'cart.html', dict(cart_items = cart_items, total	= total, counter = counter)) 


def cart_remove(request, product_id): #to remove a quantity product from cart
	cart = Cart.objects.get(cart_id = _cart_id(request))
	product = get_object_or_404(Product, id = product_id)
	cart_item = CartItem.objects.get(product = product, cart = cart)
	if cart_item.quantity > 1:
		cart_item.quantity -= 1
		cart_item.save()
	else:
		cart_item.delete()
	return redirect('cart:cart_detail')


def full_remove(request, product_id): #To remove all quantity of the product from cart
	cart = Cart.objects.get(cart_id = _cart_id(request))
	product = get_object_or_404(Product, id=product_id)
	cart_item = CartItem.objects.get(product = product, cart = cart)
	cart_item.delete()
	return redirect('cart:cart_detail')

