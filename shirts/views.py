from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import *
from django.contrib.auth import authenticate, login as loginUser
from .models import *
from django.db.models import Min
from math import floor
# Create your views here.

def home(request):
    products = Tshirt.objects.all()
    context = {'prod':products}
    return render(request, 'index.html', context)

def product_detail(request, slug):
    details = Tshirt.objects.get(slug=slug)
    for size in Tshirt.sizevariant_set.all():
        print(size.size)
    context = {'details':details}
    return render(request, 'prod_details.html', context)    

def cart(request):
    return render(request, 'cart.html')

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
                return redirect('home')

        else:
            context = {'form':form}
            return render(request, 'login.html', context)    


def logout(request):
    request.session.clear()
    return redirect('home')




def contact(request):
    return render(request, 'contact-us.html')