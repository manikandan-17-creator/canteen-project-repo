from django.shortcuts import render,get_object_or_404
from .cart import Cart 
#the product model has not been created 
#from base.models import product
from django.http import JsonResponse

# Create your views here.
def cart_summary(request):
    return render(request, 'cart/cart_summary.html')

def cart_add(request):
      # Get the cart
      cart = Cart(request)
      # test for POST
      if request.POST.get('action') == 'post':
            # Get stuff
            product_id = int(request.POST.get('product_id'))
            # lookup product in DB
            product = get_object_or_404 (Product, id=product_id)
            # Save to session
            cart.add(product-product)

            response = JsonResponse({'Product Name' : product.name})
            return response

def cart_delete(request):
    return render(request, 'cart/cart_delete.html')

def cart_update(request):
    return render(request, 'cart/cart_update.html')