from django.db import models
from shop.models import Product

class Cart(models.Model):
	cart_id = models.CharField(max_length=250, blank=True)
	date_added = models.DateField(auto_now_add=True)

	class Meta:
		db_table = 'Cart' #defining the name of the table
		ordering = ['date_added']

	def __str__(self):
		return self.cart_id


class CartItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE) #i.e if the product is deleted then any mention of that product is also deleted
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	active = models.BooleanField(default=True)

	class Meta:
		db_table = 'CartItem'

	def sub_total(self): #to calculate the total price 
		return self.product.price * self.quantity

	def __str__(self):
		return self.product
