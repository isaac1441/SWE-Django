from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed, Http404
from django.urls import reverse
from django.db import connection

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages


from .models import Post, Comment
from .forms import CommentForm
from .forms import SignUpForm, LogInForm, PostForm

User = get_user_model()


# Create your views here.

def index(request):
    print("Connected to DB:", connection.settings_dict['NAME'])
    ### 1. Get all the posts (newest first)
    all_posts = Post.objects.all().order_by('-id') # Assumes you have a 'created_at' field
    
    ### 2. Create an empty form instance for the "Add Post" form
    form = PostForm()

    ### 3. Update the context
    context = {
        'items': all_posts,  # 'items' is now your list of posts
        'form': form         # Pass the form to the template
    }
    return render(request, "app/index.html", context)

@login_required
def add_post_view(request):
    if request.method == 'POST':
        form=PostForm(request.POST)
        if form.is_valid():
            #new post created
            new_post=form.save(commit=False)

            new_post.author = request.user

            new_post.save()

            return redirect('home')
    return redirect('home')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    comments = post.comments.all().order_by('created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()

            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'form': form
    }

    return render(request, 'app/post_detail.html', context)


@login_required
def delete_post_view(request,pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        messages.error(request, "You are not authorized to delete this post")
        return redirect('home')
    
        
    post.delete()
    messages.success(request, "Post deleted successfully")
       
    return redirect('home')


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

