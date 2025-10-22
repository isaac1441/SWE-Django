from django.urls import path # type: ignore

from . import views

urlpatterns = [
    path("", views.index, name="home"), 
    path("home/", views.index, name="home"), 
    
    # account urls
    path("signup/", views.signup_view, name="signup"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("account/", views.account_view, name="account"),
    path("account/<slug:username>/", views.account_view, name="account"),
    
    # 
    # path("cart/", views.cart_view, name="cart"),
    # path("product/<slug:product_slug>/",views.product_page, name="product_page"),
    # path("product/<int:product_id>/",views.product_by_id, name="product_by_id"),

]