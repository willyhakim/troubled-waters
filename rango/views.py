#rango/views.py
from django.htpp import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

def register(request):
	"""View that handles registering a new user"""
	registered = False # A boolean value for telling the template whether the registration was successful 

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		#Check if the two forms are valid
		if user_form.is_valid() and profile_form.is_valid():
			user =user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			#Did the user provide a profile picture?
			#If so, we need to save it in the UserProfile model
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
				#Now we save the UserProfile model instance
				profile.save()
				#Update our boolean variable to tell the template registration is successful!
				registered = True
		#what do we do if form is not valid?
		#Print the problems. Event log
		#show them to the user
		else:
			print user_form.errors, profile_form.errors
	#Not an HTTP POST? Sweet! let's render the form using ModelForm instances.
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	context_dict = {'user_form':user_form, 'profile_form':profile_form, 'registered': registered}	

	return render(request, 'rango/register.html', context_dict)


def index(request):
	category_list =Category.objects.order_by('-likes')[:5]
	context_dict = {'categories':category_list}

	return render(request, 'rango/index.html', context_dict)

def category(request, category_name_slug):
	context_dict = {}

	try:
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name'] = category.name 
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		pass
	return render(request, 'rango/category.html', context_dict)

def add_category(request):
	"""View that handles the form to add more categories"""

	if request.method == 'POST':
		form = CategoryForm(request.POST)

		#validate the form
		if form.is_valid():
			form.save(commit=True)
			return index(request)
		else:
			print form.errors 

	else:
		form = CategoryForm()

	return render(request, 'rango/add_category.html', {'form':form})

def add_page(request, category_name_slug):
	"""View that handles the form to add pages to category"""
	try:
		cat = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		cat = None

	if request.method=='POST':
		form= PageForm(request.POST)
		if form.is_valid():
			if cat:
				page = form.save(commit=False)
				page.category = cat
				page.views = 0
				page.save()
				return category(request, category_name_slug)
		else:
			print form.errors

	else:
		form = PageForm()
	context_dict = {'form':form, 'category':cat}
	return render(request, 'rango/add_page.html', context_dict)

def user_login( request):
	"""View method to to login any given user"""
	if request.method == 'POST':
		#Since request.POST is a dict we can use some interesting dict methods like get!
		username  = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			# Is the account active?
			if user.is_active:
				#If the account is valid and active. What the hell, let's let the user in
				login(request, user)
				return HttpResponseRedirect('/rango/')
			else:
				#an inactive account was used - no loggin in!
				return HttpResponse("Your account is disabled")
		else:
			#Bad bad user! kick their butt to the curb!
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse('Invalid login details supplied.')

	else:
		#Not a request.Post! Oh gee, it is a get. Let's pass the form
		return render(request. 'rango/login.html', {})	



