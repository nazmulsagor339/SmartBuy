from .models import Cart

def cart_total_product(request):
    if request.user.is_authenticated:
        total_product = Cart.objects.filter(user=request.user).count()
        return {'total_product':total_product}
    else:
        return {'total_product':'Login Please'}

