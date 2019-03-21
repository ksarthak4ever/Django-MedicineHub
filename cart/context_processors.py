'''Context processors. A context processor is a Python function that takes the request object as an argument and returns a dictionary that gets added to the request context i.e makes it available throughout the site.
'''

from .models import Cart,CartItem
from .views import _cart_id
from django.core.exceptions import ObjectDoesNotExist

def counter(request): #function to get how many products are in the cart so that i can display them in the navbar cart icon
	item_count = 0
	if 'admin' in request.path:
		return{}
	else:
		try:
			cart = Cart.objects.filter(cart_id=_cart_id(request)) #getting cart_id of that session or user
			cart_items = CartItem.objects.all().filter(cart=cart[:1]) #getting all the cart items of that user
			for cart_item in cart_items:
				item_count += cart_item.quantity
		except Cart.DoesNotExist:
			item_count = 0

	return dict(item_count= item_count) #returning item_count which has the number of items in the cart for that cart_id i.e session, this will be used in the navbar

