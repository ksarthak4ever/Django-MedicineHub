from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from . models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist

import stripe #to use stripe as payment gateway
from django.conf import settings

from order.models import Order,OrderItem #to create orders


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

	stripe.api_key = settings.STRIPE_SECRET_KEY #setting up these values so i can use them in cart.html as mentions in stripe documentation
	stripe_total = int(total * 100)
	description = 'MedicineHub - New Order'
	data_key = settings.STRIPE_PUBLISHABLE_KEY
	if request.method == 'POST':
		try:
			token = request.POST['stripeToken']
			email = request.POST['stripeEmail']
			billingName = request.POST['stripeBillingName'] #to get Billing Name from stripe payment form
			billingAddress1 = request.POST['stripeBillingAddressLine1']
			billingCity = request.POST['stripeBillingAddressCity']
			billingState = request.POST['stripeBillingAddressState']
			billingPostcode = request.POST['stripeBillingAddressZip']
			billingCountry = request.POST['stripeBillingAddressCountryCode']
			shippingName = request.POST['stripeShippingName']
			shippingAddress1 = request.POST['stripeShippingAddressLine1']
			shippingCity = request.POST['stripeShippingAddressCity']
			shippingState = request.POST['stripeShippingAddressState']
			shippingPostcode = request.POST['stripeShippingAddressZip']
			shippingCountry = request.POST['stripeShippingAddressCountryCode']
			customer = stripe.Customer.create( #tokenizing the customer card as told in stripe doc
					email = email,
					source = token
				) #creating a charge
			charge = stripe.Charge.create(
					amount = stripe_total,
					currency = "inr",
					description = description,
					customer = customer.id
				)
			''' Creating the Order '''
			try:
				order_details = Order.objects.create(
						token = token,
						total = total,
						emailAddress = email, 
						billingName = billingName,
						billingAddress1 = billingAddress1,
						billingCity = billingCity,
						billingState = billingState,
						billingPostcode = billingPostcode,
						billingCountry = billingCountry,
						shippingName = shippingName,
						shippingAddress1 = shippingAddress1,
						shippingCity = shippingCity,
						shippingState = shippingState,
						shippingPostcode = shippingPostcode,
						shippingCountry = shippingCountry
					)
				order_details.save()
				for order_item in cart_items: #every time the for loop runs a cart item is assigned to the order item variable
					oi = OrderItem.objects.create(
							product = order_item.product.name,
							quantity = order_item.quantity,
							price = order_item.product.price,
							order = order_details
						) #oi variable is getting the value of each order item in order to create the order item record
					oi.save()
					'''Reduce stock when order is placed or saved'''
					products = Product.objects.get(id = order_item.product.id)
					products.stock = int(order_item.product.stock - order_item.quantity) #removing products from stock once order been completed 
					products.save()
					order_item.delete() #Once order complete the order_items will get deleted
					'''The terminal will print this message when the order is saved'''
					print('The order has been created')
				return redirect('shop:allProdCat')
			except ObjectDoesNotExist:
				pass
		except stripe.error.CardError as e:
			return False,e
	return render(request, 'cart.html', dict(cart_items = cart_items, total	= total, counter = counter, data_key = data_key, stripe_total = stripe_total, description = description)) 


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

