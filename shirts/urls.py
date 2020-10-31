from django.contrib import admin
from django.urls import path, include
from shirts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('contact/', views.contact, name='contact'),
    path('usersignup/', views.signup, name='signup'),
    path('userlogin/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
