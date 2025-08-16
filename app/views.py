from django.shortcuts import render,redirect
from django.views import View

from django.contrib import messages
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

from django.db.models import Q

from .models import Customer, Product, Cart, Order
from .forms import RegistrationForm,AddressForm,ProfileForm,LoginForm

# ------------------------------ All Product Section ------------------------------------------------------
class ProductView(View):
    def get(self,request):
        top_wear = Product.objects.filter(category='TW')
        electronics = Product.objects.filter(category='E')
        bottom_wear = Product.objects.filter(category='BW')
        mobile = Product.objects.filter(category='M')
        laptop = Product.objects.filter(category='L')
        context = {
           'top_wear':top_wear,
           'bottom_wear':bottom_wear,
           'mobile':mobile,
           'laptop':laptop,
           'electronics':electronics,
        }
        return render(request, 'app/home.html',context)
    
#-------------------------------- Single Product Section --------------------------------------------------------
class ProductDetailView(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        # if the product is already added to the cart, it'll show go to cart.And try and except is being used to solve the error.
        try:
            product_already_in_cart = Cart.objects.get(product=pk,user=request.user)
        except:
            context = {
            'product':product,
            }
            return render(request, 'app/productdetail.html',context)

        context = {
            'product':product,
            'product_already_in_cart':product_already_in_cart
            }   
        return render(request, 'app/productdetail.html',context)
    
# ------------------------ Filtering all the product according to their brand --------------------------
def electronics(request,data=None):
    if data == None:
       electronics = Product.objects.filter(category = 'E')
    # Filtering the price in LOW and HIGH 
    elif data == 'XiaomiLow':
        electronics = Product.objects.filter(category = 'E').filter(brand='Xiaomi').filter(selling_price__lte = 1000)

    elif data == 'XiaomiHigh':
        electronics = Product.objects.filter(category = 'E').filter(brand='Xiaomi').filter(selling_price__gt = 1000)

    elif data == 'Canon-DLow':
        electronics = Product.objects.filter(category = 'E').filter(brand='Canon-D').filter(selling_price__lte = 30000)

    elif data == 'Canon-DHigh':
        electronics = Product.objects.filter(category = 'E').filter(brand='Canon-D').filter(selling_price__gt = 30000)

    elif data == 'RolexLow':
        electronics = Product.objects.filter(category = 'E').filter(brand='Rolex').filter(selling_price__lte = 1000)

    elif data == 'RolexHigh':
        electronics = Product.objects.filter(category = 'E').filter(brand='Rolex').filter(selling_price__gt = 1000)

    else:
        electronics = Product.objects.filter(category = 'E').filter(brand=data)
       
    return render(request, 'app/electronics.html',{'electronics': electronics,'data':data})
    
# ------------------------------ Add to cart Section ------------------------------------------------------
@login_required(login_url='login')
def add_to_cart(request):
    cart_product = Cart.objects.filter(user = request.user).order_by('-id')
    if request.method =='POST':
        product_id = request.POST['prod_id'] #data sent from productdetail.html file 'add to cart' button.Getting the data from the url
        """ if the product already added to the cart model, this condition will prevent from adding the product multiple times. """
        if Cart.objects.filter(product = product_id).exists():
            return redirect('add-to-cart')
        else:
            product = Product.objects.get(id = product_id)
            user = request.user
            cart = Cart.objects.create(user = user, product = product)
            cart.save()
            return redirect('add-to-cart')

    else:
        amount = 0.0
        shipping = 100.0
        total = 0.0
        for object in cart_product:
            amount= amount + (object.quantity * object.product.discounted_price)
        total = amount + shipping
        return render(request, 'app/addtocart.html',{'cart':cart_product,'amount':amount,'shipping':shipping,'total':total})

# ------------------------------ add or remove product from cart -----------------------------------------------
def cart_quantity(request):

    if request.method == 'GET':
        
        # Getting product id sent through ajax from myscript.js which is actually from increase cart product quantity icon in addtocart.html
        prod_id = request.GET['prod_id']
        print("cart",prod_id)
        cart_action = request.GET['cart_action']
        product = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))

        # Getting the product which belongs to the logged user and requested to increase the product quantity
        if cart_action == '1':
            product.quantity += 1
            product.save()

        elif cart_action == '2':
            if product.quantity>1:
                product.quantity -= 1
                product.save()
        
        elif cart_action == '3':
            product.delete()

        # updating the price after increasing the product quantity
        cart_product = Cart.objects.filter(user = request.user).order_by('-id')
        amount = 0.0
        shipping = 100.0
        total = 0.0
        for object in cart_product:
            amount= amount + (object.quantity * object.product.discounted_price)
        total = amount + shipping
        data = {
            'quantity':product.quantity,
            'amount':amount,
            'total':total,
        }
        return JsonResponse(data)
    
# ----------------------------- all the order and the selected address section -------------------------- 
@login_required(login_url='login')   
def checkout(request):
    address = Customer.objects.filter(user = request.user)

    products = Cart.objects.filter(user=request.user)
    amount = 0.0
    shipping = 100.0
    total = 0.0
    for object in products:
        amount= amount + (object.quantity * object.product.discounted_price)
    total = amount + shipping

    return render(request, 'app/checkout.html',{'address':address,'products':products,'total':total})

# ---------------------------------- Product buying section --------------------------------------------------
@login_required(login_url='login')
def buy_now(request):
    # address_id is getting from address radio button in checkout.html file
    try:
        address_id = request.GET.get('customer_address')
        customer_address = Customer.objects.get(id=address_id)
    except:
        messages.error(request,'Select your address first!')
        return redirect('checkout')
    cart_product = Cart.objects.filter(user=request.user)
    for product in cart_product:
        Order(user=request.user,customer=customer_address,product=product.product,quantity=product.quantity).save()
        product.delete()
    return render(request, 'app/buynow.html')


# ---------------------------------- Order section --------------------------------------------------
@login_required(login_url='login')
def orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'orders':orders})

# ------------------------------------------ Address Section ----------------------------------------------
#-------------------------------------- Edit Address ------------------------------------------------------
@login_required(login_url='login')
def editAddress(request,pk):        
    data = Customer.objects.get(id=pk)
    if request.method == 'POST':
        form = AddressForm(request.POST,instance=data)
        if form.is_valid():
            form.save()
            messages.success(request,'Your information is updated!')
            return redirect('address_list')
    else:
        form = AddressForm(instance=data)

    return render(request, 'app/address.html',{'form':form})

#------------------------------------- Show all Address ----------------------------------------------------
@login_required(login_url='login')
def addressList(request):             
    address = Customer.objects.filter(user = request.user) 
    return render(request, 'app/address_list.html',{'address':address,})

#-------------------------------------------Delete Address --------------------------------------------------
@login_required(login_url='login')
def deleteAddress(request,pk):             
    address = Customer.objects.get(id=pk) 
    address.delete()
    messages.success(request,'Deleted successfully!!!')
    return redirect('address_list')

#------------------------------------------ Add address --------------------------------------------------------
@login_required(login_url='login')
def address(request):             
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()
            messages.success(request,'Your information is added!')
            return redirect('address_list')
        else:
            messages.error(request,'Wrong Information. Add information According to the form.')
    else:
        form = AddressForm()

    return render(request, 'app/address.html',{'form':form})


#----------------------------------- LOGIN Section is in the urls.py file -------------------------
def signout(request):
    logout(request)
    return redirect('login')

#---------------------------------------- User Registration ----------------------------------------------
def customerregistration(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            print('inside post')
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Account created successfully. Please Login now!')
                return redirect('login')
        else:
            form = RegistrationForm()
            print('inside else')
        return render(request, 'app/customerregistration.html',{'form':form})
    else:
        messages.error(request,'Logout first to register account!')
        return redirect('home')
    
# ------------------------------------------ Profile Section ----------------------------------------------
@login_required(login_url='login')
def profile(request,pk):
    if pk == 1: 
        return render(request, 'app/profile.html',{'pk':pk})
    elif pk == 2:
        user = User.objects.get(id=request.user.id)
        if request.method == 'POST':
            form = ProfileForm(request.POST,instance=user)
            print('method post')
            if form.is_valid():
                form.save()
                pk = 1
                return redirect('profile',pk=1)
            else:
                return redirect('profile',pk=1)
        else:
            form = ProfileForm(instance=user)
            return render(request, 'app/profile.html',{'pk':pk,'form':form})
        


