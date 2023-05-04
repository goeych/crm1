from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only

from . models import *
from .forms import OrderForm,CreateUserForm,CustomerForm
from .filters import OrderFilter

# Create your views here.

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form= CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user)
            #print("user:",user)
            
            messages.success(request,'Account was created for ' + username)
            return redirect('login_page')
        
    context = {'form':form}
    return render(request,'accounts/register.html',context)

@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.info(request,"username or Password is incorrect")
           
        
    context = {}
    return render(request,'accounts/login.html',context)

def logoutPage(request):
    logout(request)
    return redirect('login_page')
    
@login_required(login_url='login_page')
@admin_only
def dashboard(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    customers_count = customers.count()
    orders_count = orders.count()
    orders_delivered_count = orders.filter(status='Delivered').count()
    orders_pending_count = orders.filter(status='Pending').count()    

    
    context={'orders':orders,'customers':customers,
             'orders_count':orders_count,'orders_delivered_count':orders_delivered_count,
             'orders_pending_count':orders_pending_count,}
    
    return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    customer_ordersets = request.user.customer.order_set.all()
    print("customer_ordersets:",customer_ordersets)

    orders_count = customer_ordersets.count()  
    orders_delivered_count = customer_ordersets.filter(status='Delivered').count()
    orders_pending_count = customer_ordersets.filter(status='Pending').count()    
    
    context={'customer_ordersets':customer_ordersets,'orders_count':orders_count,
          'orders_delivered_count':orders_delivered_count,'orders_pending_count':orders_pending_count,}
    
    return render(request,'accounts/user.html',context)

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance = customer)

    if request.method == "POST":
        form = CustomerForm(request.POST,request.FILES,instance = customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request,'accounts/account_settings.html',context)



@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    
    context={'products':products}
    
    return render(request,'accounts/products.html',context)

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def customers(request,pk):
    customer = Customer.objects.get(id=pk)
    customer_ordersets = customer.order_set.all()
    customer_ordersets_count =customer_ordersets.count()

    myFilter = OrderFilter(request.GET,queryset=customer_ordersets)
    customer_ordersets = myFilter.qs
    
    context={'customer':customer,
             'customer_ordersets':customer_ordersets,
             'customer_ordersets_count':customer_ordersets_count,
             'myFilter':myFilter,
             }

    print('customer_ordersets_count',customer_ordersets_count)
    
    return render(request,'accounts/customers.html',context)

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('customer','product','status'),extra=2)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    #queryset=Order.objects.none()//disable the existing record

    #form =OrderForm(initial={'customer':customer})
    if request.method =='POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('dashboard')

    context={'formset':formset}

    return render(request,'accounts/order_form.html',context)

@login_required(login_url='accounts:login_page')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order =Order.objects.get(id=pk)
    form =OrderForm(instance=order)

    if request.method =='POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

   
    context={'form':form}

    return render(request,'accounts/update_form.html',context)

@login_required(login_url='accounts:login_page')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order =Order.objects.get(id=pk)
    if request.method =='POST':
        order.delete()
        return redirect('dashboard')

    context={'order':order}
    return render(request,'accounts/delete.html',context)
    


