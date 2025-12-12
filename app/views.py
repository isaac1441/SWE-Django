from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed, Http404
from django.urls import reverse
from django.db import connection
from django.db.models import OuterRef, Subquery
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages


from .models import Post, Comment, Profile
from .forms import CommentForm
from .forms import SignUpForm, LogInForm, PostForm

User = get_user_model()


# Create your views here.

def index(request):
    first_comment = (
        Comment.objects
               .filter(post=OuterRef('pk'))
               .order_by('created_at')
    )

    items = (
        Post.objects
            .order_by('-id')  
            .annotate(
                first_comment_body   = Subquery(first_comment.values('body')[:1]),
                first_comment_author = Subquery(first_comment.values('author__username')[:1]),
                first_comment_time   = Subquery(first_comment.values('created_at')[:1]),
            )
    )

    return render(request, "app/index.html", {"items": items, "form": PostForm()})

@login_required
def add_comment_view(request):
    if request.method == 'POST':
        form=PostForm(request.POST)
        if form.is_valid():
            new_post=form.save(commit=False)

            new_post.author = request.user

            new_post.save()

            return redirect('home')
    return redirect('home')

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
    else:
        form = PostForm()
    return render(request, 'app/create_post.html', {'form':form})

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

@login_required
def my_profile_redirect(request):
    return redirect("profile", username=request.user.username)

def profile_view(request, username):
    # Whose profile are we viewing?
    profile_user = get_object_or_404(User, username=username)

    # Make sure a Profile exists for them
    profile_obj, _ = Profile.objects.get_or_create(user=profile_user)

    is_own_profile = request.user.is_authenticated and (request.user == profile_user)

    # Is the current user following this profile?
    is_following = False
    if request.user.is_authenticated and not is_own_profile:
        viewer_profile, _ = Profile.objects.get_or_create(user=request.user)
        is_following = viewer_profile.following.filter(pk=profile_obj.pk).exists()

    context = {
        "profile_user": profile_user,
        "profile_obj": profile_obj,
        "is_own_profile": is_own_profile,
        "is_following": is_following,
        # use the actual relations, not missing properties
        "followers_count": profile_obj.followers.count(),
        "following_count": profile_obj.following.count(),
    }
    return render(request, "app/profile.html", context)


@login_required
def follow_user(request, username):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    target_user = get_object_or_404(User, username=username)

    # Don’t allow following yourself
    if target_user == request.user:
        return redirect("profile", username=username)

    follower_profile, _ = Profile.objects.get_or_create(user=request.user)
    target_profile, _ = Profile.objects.get_or_create(user=target_user)

    follower_profile.follow(target_profile)

    messages.success(request, f"You are now following {target_user.username}.")
    return redirect("profile", username=username)


@login_required
def unfollow_user(request, username):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    target_user = get_object_or_404(User, username=username)

    if target_user == request.user:
        return redirect("profile", username=username)

    follower_profile, _ = Profile.objects.get_or_create(user=request.user)
    target_profile, _ = Profile.objects.get_or_create(user=target_user)

    follower_profile.unfollow(target_profile)

    messages.success(request, f"You unfollowed {target_user.username}.")
    return redirect("profile", username=username)


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
    next_url = request.META.get('HTTP_REFERER', 'home')
    return redirect(next_url)

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

