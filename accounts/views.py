from django.db import models
from django.forms.models import inlineformset_factory
from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.models import Customer, Order, Product

from django.forms import inlineformset_factory
from .filters import OrderFilter
from .forms import RegistrationForm, OrderForm, CustomerForm
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only_or_customer
from django.contrib.auth.models import User, Group

# Create your views here.

@unauthenticated_user
def registerPage(request):
  
    form = RegistrationForm()
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created sucessfully for' + " "+ username)
            group = Group.objects.get(name = 'customer')
            user.groups.add(group)
            #messages.success(request, "Added to customer group sucesfully")
            Customer.objects.create(user=user) # automatically add to a group when a new user signsup. we have our user field in Customer model
            
            
            return redirect('login')
    context = {'form':form}
    return render(request, 'registration.html', context)
 
@unauthenticated_user
def loginPage(request):
  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        
            return redirect('home')
        else:
            messages.info(request, 'Username or password is not matching ')
    context = {}
    return render(request, 'login.html', context)



def logoutPage(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
@admin_only_or_customer
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    pending_count = orders.filter(status='Pending').count()
    delivered_count = orders.filter(status ='Delivered').count()
    
    
    
    context = {'customers':customers, 'orders': orders, 'total_customers': total_customers, 'total_orders': total_orders, 'pending_count': pending_count, 'delivered_count': delivered_count}
    return render(request, 'dashboard.html',context)

#@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})
   
@login_required(login_url='login')
def customers(request,id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'customer': customer, 'orders':orders, 'myFilter': myFilter}
    return render(request, 'customers.html', context)    


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def createOrder(request,id):
    OrderFormSet = inlineformset_factory(Customer,Order, fields=('product', 'status'))
    customer = Customer.objects.get(id=id)
    formset =OrderFormSet(instance=customer)
    #form =OrderForm(initial={'customer': customer})
    if request.method =='POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset': formset}
    return render(request,'order_form.html', context )


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateORder(request, id):
    order = Order.objects.get(id = id)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, id):
    order = Order.objects.get(id = id)
    if request.method =='POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'delete.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    
    orders = request.user.customer.order_set.all()
    total_order = orders.count()
    delivered = orders.filter(status ='Delivered').count()
    pending = orders.filter(status = 'Pending').count()
    
    context = {"orders": orders, "total_order": total_order, "delivered": delivered, "pending": pending}
    return render(request, 'userpage.html', context)


def accountSettings(request):
    user = request.user.customer
    form = CustomerForm( instance= user)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance= user)
        if form.is_valid():
            form.save()
            
    
    context ={'form': form}
    return render(request, 'account-setting.html', context)    