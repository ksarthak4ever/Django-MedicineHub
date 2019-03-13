from django.db import models
from django.urls import reverse


class Category(models.Model): #Category of Medicine
	name = models.CharField(max_length=255, unique=True)
	slug = models.SlugField(max_length=255, unique=True) #this is the url path that reciever requests on the browser.
	description = models.TextField(blank=True)
	image = models.ImageField(upload_to='category',blank=True) #upload to category folder when new category is made.

	class Meta:
		ordering = ('name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def get_url(self):
		return reverse('shop:products_by_category', args=[self.slug])

	def __str__(self):
		return '{}'.format(self.name)


class Product(models.Model): #model for Medicine Products
	name = models.CharField(max_length=255, unique=True)
	slug = models.SlugField(max_length=255, unique=True)
	description = models.TextField(blank=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	image = models.ImageField(upload_to='product', blank=True)
	stock = models.IntegerField()
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'product'
		verbose_name_plural = 'products'

	def get_url(self):
		return reverse('shop:ProdCatDetail', args=[self.category.slug, self.slug])

	def __str__(self):
		return '{}'.format(self.name)