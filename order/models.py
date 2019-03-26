from django.db import models


class Order(models.Model):
	token = models.CharField(max_length=255, blank=True)
	total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='INR Order Total')
	emailAddress = models.EmailField(max_length=250, blank=True, verbose_name='Email Address')
	created = models.DateTimeField(auto_now_add = True)
	billingName = models.CharField(max_length = 250, blank = True)
	billingAddress1 = models.CharField(max_length = 250, blank = True)
	billingCity = models.CharField(max_length = 250, blank = True)
	billingState = models.CharField(max_length = 5, blank = True)
	billingPostcode = models.CharField(max_length = 10, blank = True)
	billingCountry = models.CharField(max_length = 200, blank = True)
	shippingName = models.CharField(max_length = 250, blank = True)
	shippingAddress1 = models.CharField(max_length = 250, blank = True)
	shippingCity = models.CharField(max_length = 250, blank = True)
	shippingState = models.CharField(max_length = 5, blank = True)
	shippingPostcode = models.CharField(max_length = 10, blank = True)
	shippingCountry = models.CharField(max_length = 200, blank = True)

	class Meta:
		db_table = 'Order'
		ordering = ['-created']

	def __str__(self):
		return str(self.id) #returning order id in str format


class OrderItem(models.Model):
	product = models.CharField(max_length = 250)
	quantity = models.IntegerField()
	price = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name = 'INR Price')
	order = models.ForeignKey(Order, on_delete = models.CASCADE)

	class Meta:
		db_table = 'OrderItem'

	def sub_total(self):
		return self.quantity * self.price

	def __str__(self):
		return self.product

