from django.shortcuts import render, redirect
from .models import Product, Cart
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ProductForm
from django.http import JsonResponse
# Create your views here.

def index(request):
    if request.user.is_authenticated():
        x = Product.objects.exclude(cart_product__user=request.user).exclude(seller=request.user).order_by('-timestamp')
        query = request.GET.get("q")
        if query:
            x = x.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(seller__first_name__icontains=query) |
                Q(seller__last_name__icontains=query) |
                Q(category__icontains=query) |
                Q(campus__icontains=query) |
                Q(state__icontains=query) |
                Q(selling_type__icontains=query)
            ).distinct()
        begin = request.GET.get('from')
        end = request.GET.get('to')
        if begin and end:
                x = x.filter(
                Q(price__gte=begin) &
                Q(price__lte=end)
            ).distinct()
        return render(request, 'index.html', {'products':x})
    else:
        x = Product.objects.all()
        return render(request, 'index.html', {'products':x})



@login_required
def my_products(request):
    x = Product.objects.filter(seller=request.user)
    query = request.GET.get("q")
    if query:
        x = x.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(seller__first_name__icontains=query) |
            Q(seller__last_name__icontains=query) |
            Q(category__icontains=query) |
            Q(campus__icontains=query) |
            Q(state__icontains=query) |
            Q(selling_type__icontains=query)
        ).distinct()
    return render(request, 'shop.html', {'products':x, 'active':'active'})

@login_required
def delete_product(request,slug):
    x = Product.objects.get(slug=slug)
    x.delete()
    return redirect('/my-products')

@login_required
def category(request, category):
    x = Product.objects.filter(category=category).exclude(cart_product__user=request.user)
    return render(request, 'index.html', {'products':x})

@login_required
def add_product(request, slug):
    product = Product.objects.get(slug=slug)
    user = request.user
    obj, created = Cart.objects.get_or_create(user=user, product=product, completed=False)
    cart_objects = Cart.objects.filter(user=request.user)
    all_selling = request.user.selling.all()
    sell_cart = Cart.objects.filter(product__in=all_selling)
    return render(request, 'cart.html', {'cart_objects':cart_objects, 'sell_cart':sell_cart})
    

@login_required
def sell_form(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        new_product = form.save(commit=False)
        new_product.seller = request.user
        new_product.save()
        return redirect('/my-products')


    context = {
        'title': 'Selling Form',
        'form': form
    }
    return render(request, 'form.html', context)

def shop(request):
    return render(request, 'shop.html', {})

def product_detail(request, slug):
    product = Product.objects.get(slug=slug)

    x = product.seller == request.user
    
    return render(request, 'product-details.html', {'product':product, 'seller':x})

def cart(request):
    buy_cart = Cart.objects.filter(user=request.user)
    all_selling = request.user.selling.all()
    sell_cart = Cart.objects.filter(product__in=all_selling)
    return render(request, 'cart.html', {'cart_objects':buy_cart, 'sell_cart':sell_cart})

def delete_cart(request, username, slug):
    user = User.objects.get(username=username)
    product = Product.objects.get(slug=slug)
    cart_object = Cart.objects.get(user=user, product=product)
    cart_object.delete()
    return redirect('/cart')


def login_signup(request):
    return render(request, 'login.html', {})

def contact(request):
    return render(request, 'contact-us.html', {})
