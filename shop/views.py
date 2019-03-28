from django.shortcuts import render,get_object_or_404, redirect
from . models import Category,Product
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from django.contrib.auth.models import Group, User
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout


#Category view

def allProdCat(request, c_slug=None): #Used to show all products in that category
	c_page = None #for categories
	products_list = None
	if c_slug!=None:
		c_page = get_object_or_404(Category,slug=c_slug)
		products_list = Product.objects.filter(category=c_page,available=True) #filtering products according to category 
	else:
		products_list = Product.objects.all().filter(available=True)
	''' Paginator Code '''
	paginator = Paginator(products_list,6) #limiting 6 products per category page
	try:
		page = int(request.GET.get('page','1')) #converting GET request to integer i.e page number 1 so we can store it in page variable
	except:
		page = 1
	try:
		products = paginator.page(page) 
	except (EmptyPage, InvalidPage):
		products = paginator.page(paginator.num_pages)
	return render(request,'shop/category.html',{'category':c_page,'products':products})


#Product View

def ProdCatDetail(request, c_slug, product_slug): #Used to show detail product view
	try:
		product = Product.objects.get(category__slug=c_slug, slug=product_slug)
	except Exception as e:
		raise e
	return render(request, 'shop/product.html', {'product':product})


#Forms View

def signupView(request): #Used to create an account for the User
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid(): # checking if form details entered are valid or not
			form.save()
			username = form.cleaned_data.get('username')
			signup_user = User.objects.get(username = username)
			customer_group = Group.objects.get(name = 'Customer')  
			customer_group.user_set.add(signup_user)
	else:
		form = SignUpForm()
	return render(request, 'accounts/signup.html', {'form':form})	


def signinView(request): #Used to login user 
	if request.method == 'POST':
		form = AuthenticationForm(data = request.POST) 
		if form.is_valid():
			username = request.POST['username'] #getting username and password from the form
			password = request.POST['password']
			user = authenticate(username = username, password = password)
			if user is not None: #checking if username and password are authenticated 
				login(request, user)
				return redirect('shop:allProdCat')
			else:
				return redirect('signup')
	else:
		form = AuthenticationForm()
	return render(request, 'accounts/signin.html', {'form':form})


def signoutView(request):
	logout(request)
	return redirect('signin')
