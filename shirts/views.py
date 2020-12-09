from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .forms import *
from django.contrib.auth import authenticate, login as loginUser
from .models import *
from django.db.models import Min
from math import floor
from django.http.response import HttpResponse, HttpResponseRedirect
from django.http import request
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from store.settings import API_KEY, AUTH_TOKEN 
from instamojo_wrapper import Instamojo


API = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/');


# Create your views here.
def handler404(request):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)
    
def home(request):
    products = Tshirt.objects.all()
    context = {'prod':products}
    return render(request, 'index.html', context)


def allprod(request):
    query = request.GET
    products = []
    products = Tshirt.objects.all()

    prodbrand = query.get('prodbrand')
    occ = query.get('occ')
    prodcolor = query.get('color')
    sleeve = query.get('sleeve')
    neck = query.get('neck')
    ideal = query.get('ideal')

    if prodbrand !='' and prodbrand is not None:
        products = products.filter(brand__slug=prodbrand)

    if neck !='' and neck is not None:
        products = products.filter(neck__slug=neck)
    
    if prodcolor !='' and prodcolor is not None:
        products = products.filter(color__slug=prodcolor)
    
    if occ !='' and occ is not None:
        products = products.filter(occassion__slug=occ)
    
    if sleeve !='' and sleeve is not None:
        products = products.filter(sleeve__slug=sleeve)

    if ideal !='' and ideal is not None:
        products = products.filter(ideal__slug=ideal)
  

    occ = Occassion.objects.all()
    sleeve = Sleeve_type.objects.all()
    neck = Neck_type.objects.all()
    ideal = Ideal_for.objects.all()
    brands = brand.objects.all()
    colors = color.objects.all()
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {'prod':products, 'products':products, 'occ':occ, 'sleeve':sleeve, 'neck':neck, 'ideal':ideal, 'brand':brands, 'colors':colors, 'page':page }
    return render(request, 'all.html', context)        



def product_detail(request, slug):
    details = Tshirt.objects.get(slug=slug)
    size = request.GET.get('size')
    if size is None:
        size = details.sizevariant_set.all().order_by('price').first()
    else:
        size = details.sizevariant_set.get(size=size)
    size_price = size.price
    sell_price = floor(size_price - (size_price * (details.discount)/100)) #This is discount equation
    context = {'details':details, 'price':size_price, 'sell_price':sell_price, 'active_size':size,}
    return render(request, 'prod_details.html', context)    

def addtocart(request, size, slug):
    user = None
    if request.user.is_authenticated:
        user = request.user
    cart = request.session.get('cart')
    if cart is None:
        cart = []

    tshirt = Tshirt.objects.get(slug=slug)
    # size_temp = Sizevariant.objects.get(size = size, tshirt = tshirt)
    add_cart_for_anom_user(cart,  size, tshirt)

#This existing command will check that if any product is already saved in database, so it checks in the database related to the user and if any product is found with same size so this will increase its quantity of that product in the database.
    if user is not None:
        add_cart_to_database(user, size, tshirt)

    request.session['cart'] = cart
    return_url = request.GET.get('return_url')   
    return redirect(return_url)

#This method is call when user is login and save the data in the database
def add_cart_to_database(user, size, tshirt):
    size = Sizevariant.objects.get(size = size, tshirt = tshirt)
    existing = Cart.objects.filter(user = user, sizevariant = size)
    if len(existing) > 0:
        obj = existing[0]  # This means zero index mtlb jo sbse pehle hoga whi waala
        obj.quantity = obj.quantity + 1 #if quantity of any product is already exist with the same size so its quantity will increase in the cart.
        obj.save()

    else:
        c = Cart()  # Cart object is creating here 
        c.sizevariant = size  # here we are getting the size of the tshirt
        c.user = user        
        c.quantity = 1
        c.save()


def add_cart_for_anom_user(cart, size, tshirt):
    flag = True
    for cart_obj in cart:
            t_id = cart_obj.get('tshirt')
            size_short = cart_obj.get('size')
            if t_id == tshirt.id and size==size_short:
                flag = False
                cart_obj['quantity'] = cart_obj['quantity'] + 1

    if flag:
        cart_obj = {
        'tshirt': tshirt.id,
        'size': size,
        'quantity': 1,
        }
        cart.append(cart_obj)


def cart(request):
    cart = request.session.get('cart')
    if cart is None:
        return HttpResponse("Your Cart is Empty")

    for c in cart:
        tshirt_id = c.get('tshirt')
        tshirt = Tshirt.objects.get(id=tshirt_id)
        c['size'] = Sizevariant.objects.get(tshirt=tshirt_id, size=c['size'])
        c['tshirt'] = tshirt

    return render(request, 'cart.html', {'cart':cart})        
    
        


def signup(request):
    if (request.method == 'GET'):
        form = CustomerCreationForm()
        context = {'form':form}
        return render(request, 'signup.html', context)
    else:
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = user.username
            user.save()
            return render(request, 'signup.html')
    context = {'form':form}
    return render(request, 'signup.html', context)

def login(request):
    if request.method == 'GET':
        form = Customerloginform() #This comes from forms.py
        #for url
        next_page = request.GET.get('next')
        if next_page is not None:
            request.session['next_page'] = next_page            
        context = {'form':form}
        return render(request, 'login.html', context)

    else:
        form = Customerloginform(data=request.POST) #This comes from forms.py
        if form.is_valid():
            username = form.cleaned_data.get('username')    
            password = form.cleaned_data.get('password')    
            user = authenticate(username=username, password=password)

            if user:
                loginUser(request, user) #We use loginUser here because yaha 2 login ho gye hai to alag se import kiya hai isko humne

#This function is for when user is not login and add some products so, this will add cart products in the database after log in so both cart merge before login and after login(already added by user in the database) 
                session_cart = request.session.get('cart')
                if session_cart is None:
                    session_cart = []

                else:
                    for c in session_cart:
                        size = c.get('size')
                        tshirt_id = c.get('tshirt')
                        quantity = c.get('quantity')
                        cart_obj = Cart()
                        cart_obj.sizevariant = Sizevariant.objects.get(size=size, tshirt= tshirt_id)
                        cart_obj.quantity = quantity
                        cart_obj.user = user
                        cart_obj.save()



                cart = Cart.objects.filter(user = user)
                session_cart = []
                for c in cart:
                    obj = {
                        'size': c.sizevariant.size,
                        'tshirt': c.sizevariant.tshirt.id,
                        'quantity': c.quantity,
                    }
                    session_cart.append(obj)
            request.session['cart'] = session_cart
            next_page = request.session.get('next_page')
            if next_page is None:
                next_page = 'home'
            return redirect(next_page)

        else:
            context = {'form':form}
            return render(request, 'login.html', context)    


def logout(request):
    request.session.clear()
    return redirect('home')

def contact(request):
    return render(request, 'contact-us.html')

#utility function only for capture total amount of the cart
def cart_total_price(cart): #for cart total price
    total = 0
    for c in cart:
        # tshirt_object = Tshirt.objects.get(id=c.get('tshirt')) 
        # size_object = Sizevariant.objects.get(size=c.get('size'), tshirt = tshirt_object) 
        discount = c.get('tshirt').discount
        price = c.get('size').price
        final_price = floor(price - (price * (discount/100)))
        total_of_single_product = final_price * c.get('quantity')
        total = total + total_of_single_product
    return total


@login_required(login_url='/userlogin/')
def checkout(request):
    if request.method == 'GET':
        form = CheckoutForm()
        cart = request.session.get('cart')
        if cart is None:
            cart = []

        for c in cart:
            size_str = c.get('size')    
            tshirt_id = c.get('tshirt')
            quantity = c.get('quantity')
            size_obj = Sizevariant.objects.get(size=size_str, tshirt=tshirt_id)    
            c['size'] = size_obj    
            size_obj.quantity = quantity    
            c['tshirt'] = size_obj.tshirt    
        return render(request, 'checkout.html', {'form':form, 'cart':cart})
    else:
        #Post request 
        form = CheckoutForm(request.POST)
        #This is for capture the current user
        user = None
        if request.user.is_authenticated:
            user = request.user

        if form.is_valid():
            #if form is correct then we go for payment
            cart = request.session.get('cart')
            if cart is None:
                cart = []
            for c in cart:
                size_str = c.get('size')    
                tshirt_id = c.get('tshirt')
                quantity = c.get('quantity')
                size_obj = Sizevariant.objects.get(size=size_str, tshirt=tshirt_id)    
                c['size'] = size_obj    
                size_obj.quantity = quantity    
                c['tshirt'] = size_obj.tshirt    

            address = form.cleaned_data.get('shipping_address')
            phone = form.cleaned_data.get('phone')
            payment_method = form.cleaned_data.get('payment_method')
            total = cart_total_price(cart)
            # print(address, phone, payment_method, total)
            #Now create order and save order
            orders = order()
            orders.shipping_address = address
            orders.phone = phone
            orders.payment_method = payment_method
            orders.total = total
            orders.order_status = "PENDING"
            orders.user = user
            orders.save()

            #Now saving the order items in the database
            for c in cart:
                order_items = order_item()
                order_items.Order = orders  #mtlb kis order ka order_item hai ye 
                size = c.get('size')
                tshirt = c.get('tshirt')
                order_items.price = floor(size.price - (size.price * (tshirt.discount/100)))
                order_items.quantity = c.get('quantity')
                order_items.size = size
                order_items.tshirt = tshirt
                order_items.save()

            if payment_method == 'ONLINE':                    
                
                # Create a new Payment Request
                response = API.payment_request_create(
                amount=orders.total,
                purpose="Payment For Tshirts",
                send_email=True,
                buyer_name=f'{user.first_name} {user.last_name}',
                email=user.email,
                redirect_url="http://localhost:8000/validate_payment"
                )
                
                print(response['payment_request'])
                payment_request_id = response['payment_request']['id']
                url = response['payment_request']['longurl']

                payments = Payment()
                payments.Order = orders
                payments.payment_request_id = payment_request_id
                payments.save()
                return redirect(url) #this url comes from the long url

            else:
                finalorders = orders
                finalorders.order_status = 'PLACED'
                finalorders.save()
                cart = []
                request.session['cart'] = cart
                Cart.objects.filter(user=user).delete()
                return redirect('orders')    
        else:
            return redirect('checkout')    

def validate_payment(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
    payment_request_id = request.GET.get('payment_request_id')
    payment_id = request.GET.get('payment_id')
    print(payment_request_id,payment_id)
    response = API.payment_request_payment_status(payment_request_id, payment_id)
    print(response)
    status = response.get('payment_request').get('payment').get('status')
    print(status)

    if status != "Failed":
        print('Payment Success')
        try:
            payments = Payment.objects.get(payment_request_id=payment_request_id)
            payments.payment_id = payment_id
            payments.payment_status = status
            payments.save()

            finalorders = payments.Order
            finalorders.order_status = 'PLACED'
            finalorders.save()
            cart = []
            request.session['cart'] = cart
            Cart.objects.filter(user=user).delete()
        except:
            return render(request, 'payment_failed.html')

    else:
        return render(request, 'payment_failed.html')    
    return redirect(orders)

@login_required
def orders(request):
    user = request.user
    orders = order.objects.filter(user=user).order_by('-date').exclude(order_status='PENDING')
    context = {'order':orders}
    return render(request, 'orders.html', context)    


@login_required(login_url='/admin_login/')
def admin_dashboard(request):
    tshirtcount = Tshirt.objects.all().count()
    ordercount = order.objects.all().count()
    usercount = User.objects.all().count()
    context = {'tshirtcount':tshirtcount, 'order':ordercount, 'user':usercount}
    return render(request, 'webadmin/index.html', context)


def admin_login(request):
    if request.method == 'GET':
        form = Adminloginform() #This comes from forms.py
        context = {'form':form}
        return render(request, 'webadmin/admin_login.html', context)
    else:
        form = Adminloginform(data=request.POST) #This comes from forms.py
        if form.is_valid():
            username = form.cleaned_data.get('username')    
            password = form.cleaned_data.get('password')    
            user = authenticate(username=username, password=password)
            if user:
                loginUser(request, user) #We use loginUser here because yaha 2 login ho gye hai to alag se import kiya hai isko humne
            messages.success(request, "Welcome Sir")    
            return redirect('admin_dashboard')    
        else:
            context = {'form':form}
            return render(request, 'webadmin/admin_login.html', context)


def edit_product(request, id):
    if request.method == 'POST':
        tshirt = Tshirt.objects.get(id=id)
        editproductForm= EditproductForm(request.POST, instance=tshirt)
        if editproductForm.is_valid():
            editproductForm.save()
        messages.success(request, "Product Update Sucessfully !!")
        return redirect('all_products')
    else:
        tshirt = Tshirt.objects.get(id=id)
        editproductForm= EditproductForm(instance=tshirt)

    return render(request, "webadmin/edit_product.html", {'editproduct':editproductForm})


def all_products(request):
    all_prod = Tshirt.objects.all()
    context = {'prod':all_prod}
    return render(request, 'webadmin/products.html', context)

def delete_product(request, id):
    delete = Tshirt.objects.get(pk=id)  #pk means primary key
    delete.delete()
    messages.success(request, "Product Deleted Successfully.")
    
    return redirect('all_products')

def all_users(request):
    allusers = User.objects.all()
    context = {'allusers':allusers}
    return render(request, 'webadmin/users.html', context) 

# Add Product and it's Types by Custom Admin Panel

def add_brand(request):
    brand= brandform()
    if request.method=='POST':
        brand=brandform(request.POST, request.FILES)
        if brand.is_valid():
            brand.save()
        messages.success(request, "Brand Added Sucessfully !!")    
        return redirect('all_products')
    return render(request, "webadmin/brand.html", {'brand':brand})

def add_occassion(request):
    occassion= Occassionform()
    if request.method=='POST':
        occassion=Occassionform(request.POST, request.FILES)
        if occassion.is_valid():
            occassion.save()
        messages.success(request, "Occassion Added Sucessfully !!")    
        return redirect('all_products')
    return render(request, "webadmin/occassion.html", {'occassion':occassion})

def add_neck(request):
    neck= neckform()
    if request.method=='POST':
        neck=neckform(request.POST, request.FILES)
        if neck.is_valid():
            neck.save()
        messages.success(request, "neck Added Sucessfully !!")    
        return redirect('all_products')
    return render(request, "webadmin/neck.html", {'neck':neck})

def add_color(request):
    color= colorform()
    if request.method=='POST':
        color=colorform(request.POST, request.FILES)
        if color.is_valid():
            color.save()
        messages.success(request, "color Added Sucessfully !!")    
        return redirect('all_products')
    return render(request, "webadmin/color.html", {'color':color})

def add_product(request):
    productForm= ProductForm()
    productsizeForm = ProductsizeForm()
    if request.method=='POST':
        productForm=ProductForm(request.POST, request.FILES)
        productsizeForm=ProductsizeForm(request.POST, request.FILES)
        if productForm.is_valid() and productsizeForm.is_valid():
            a = productForm.save()
            b = productsizeForm.save(commit=False)
            b.foreignkeytoA = a
            b.save()
        return redirect('all_products')
    return render(request, "webadmin/add_product.html", {'product':productForm, 'productsizeForm':productsizeForm})

@login_required
def updateprofile(request):
    # u_form = UserUpdateForm()
    if request.method == 'POST':
        forms = UserUpdateForm(request.POST,instance=request.user)
        if forms.is_valid():
            forms.save()
        messages.success(request,'Your Profile has been updated!')
        return redirect('home')
    else:
        forms = UserUpdateForm(instance=request.user)

    context={'forms': forms}
    return render(request, 'updateprofile.html',context )


def profile(request):
    # users = User.objects.get(username=username)
    users = user = get_object_or_404(User, id=request.user.id)

    return render(request, 'profile.html', {'users':users})

