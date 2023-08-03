from django.shortcuts import render
from .models import Product, SearchQuery
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
# Create your views here.
def index(request):


    products_object=Product.objects.all()
    item_name = request.GET.get('item-name')
    if item_name != '' and item_name is not None:
        products_object = Product.objects.filter(title__icontains =item_name )
       

    return render(request, 'shop/index.html', {'product_object': products_object})


def detail(request,myid):
    products_object = Product.objects.get(id=myid)
    return render(request,'shop/detail.html',{'product': products_object})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Cart, CartItem
from shop.models import Product
from decimal import Decimal

User = get_user_model()

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        # Utilisateur authentifié
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Utilisateur non authentifié, vérifier si un panier temporaire est déjà créé pour la session
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(user=None)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    cart.total = sum(item.subtotal for item in cart.cartitem_set.all())
    cart.save()

    return redirect('cart')





def view_cart(request):
    # Récupérer l'utilisateur actuel
    user = request.user

    # Vérifier si l'utilisateur est authentifié
    if user.is_authenticated:
        # Utilisateur authentifié, récupérer le panier lié à l'utilisateur
        cart, created = Cart.objects.get_or_create(user=user)
    else:
        # Utilisateur anonyme, créer un nouveau panier sans utilisateur
        cart, created = Cart.objects.get_or_create(user=None)

    cart_items = cart.cartitem_set.all()

    return render(request, 'shop/cart.html', {'cart': cart, 'cart_items': cart_items})

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart = cart_item.cart

    # Soustraire le prix du produit du total du panier

    cart.total -= cart_item.subtotal
    cart_item.delete()
    cart.save()

    return redirect('cart')
