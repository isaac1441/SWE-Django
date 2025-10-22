from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from .models import Post
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse
from django.views import generic
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from .forms import SignUpForm, LogInForm
# from .models import 
from django.db import connection

# Create your views here.

def index(request):
    print("Connected to DB:", connection.settings_dict['NAME'])
    # items = Post.objects.all()
    users = User.objects.all()
    context = {'items': users}
    return render(request, "app/index.html", context)

def account_view(request):
    user = request.user
    return render(request, 'app/account.html', {'account': user})

def signup_view(request):
    if request.user.is_authenticated:
            return render(request, "app/index.html", {
                "message": "You're already logged in"})
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username, email, password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    
    return render(request, "app/signup.html", {'form': form})
        
def login_view(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            password = form.cleaned_data['password']

            try:
                user_obj = User.objects.get(email=identifier)
                username = user_obj.username
            except User.DoesNotExist:
                username = identifier

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid login credentials")
    else:
        form = LogInForm()

    return render(request, "app/login.html", {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

# def cart_view(request, cart):
#     return render(request, 'app/cart.html', {'cart': cart})

# def product_page(request, product_slug):
#    products = clothing_item.objects.filter(slug=product_slug).order_by('id')   
#    product = products.first()
#    if not product:
#        raise Http404("No product found")
#    return render(request, "store/product-page.html", {'product': product})

# def product_by_id(request, product_id):
#     product = get_object_or_404(clothing_item, id=product_id)
#     return render(request, 'store/product-page.html', {'product': product})

