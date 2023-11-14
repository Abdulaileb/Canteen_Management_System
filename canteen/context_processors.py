from .models import CartItem

def cart_processor(request):

    if request.user.is_authenticated:
        cart_item_count = CartItem.objects.filter(user=request.user).count()
       
    else:
        cart_item_count = 0
    return {'cart_item_count': cart_item_count}
