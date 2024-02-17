from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from frontmain.models import Order, OrderData, PayInfo, Moderators, TestModel
from billing.models import PayData
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from frontmain.forms import OrderCreationForm, OrderDetailsForm, ModMessagesForm
from datetime import timedelta
from django_daraja.mpesa.core import MpesaClient
from django.views.decorators.http import require_POST
#import datetime
from datetime import datetime, timezone
from django.contrib import messages

import time

# Create your views here.

def homepage(request):
    return render(request, 'frontmain/index.html')

def dash(request):
    if request.user.is_authenticated:
        return redirect('order-list-view')
    else:
        return render(request, 'frontmain/dash.html')



def extender(request):
    return render(request, 'frontmain/main.html')
@login_required
def newOrder(request):
    if request.method == "POST":
        form = OrderCreationForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('order_detail', obj.id)
        else:
            form = OrderCreationForm()
    context = {'form': OrderCreationForm()}
    return render(request, 'frontmain/newOrder.html', context)



def createOrder(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        pages = request.POST['pages']
        hours = request.POST['hours']
        days = request.POST['days']
        title = request.POST['title']
        user = request.user

        new_order = Order(subject=subject, pages=pages, hours=hours, days=days, title=title, user=user)
        new_order.save()
        return redirect('https://www.youtube.com/')
    else:
        return render(request, 'frontmain/createOrder.html')

@login_required
def OrderDetail(request, id):
    order = Order.objects.get(id=id)
    paid = PayData.objects.filter(order=order).values_list('created_at', flat = True)
    form = OrderDetailsForm()
    orderinfo = OrderData.objects.filter(order=order)
    # if order.time_paid:
    #     order_hours = order.hours
    #     order_days = order.days
    #     deadline = order.time_paid + timedelta(days=order_days, hours=order_hours)
    # else:
    #     deadline = None
        

    # if paid:
    #     time_paid = paid[0]
    #     order_hours = order.hours
    #     order_days = order.days
    #     #deadline = order.created_at + timedelta(days=order_days, hours=order_hours)
    #     deadline = time_paid + timedelta(days=order_days, hours=order_hours)
    #     time_now = datetime.now(timezone.utc)
    #     time_diff = deadline - time_now
    #     time_left = '1'
    #     time_left1 = 1
    #     print(deadline)
    

    # else:
    #     time_left = 1
    #     time_left1 = 1
    cost = order.pages * 300
    words = order.pages * 275
    if request.method == "POST":
        form = OrderDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.order = order
            obj.save()
            return redirect('order_detail', order.id)
        else:
            form = OrderDetailsForm()
    return render(request, 'frontmain/OrderDetail.html', {
        'order':order, 
        'form':form, 
        # 'time_left':time_left,
        # 'time_left1':time_left1, 
        'orderinfo':orderinfo, 
        'cost':cost, 
        'words':words, 
        'paid':paid,
        #'deadline':deadline
        })

@login_required
def OrderListView(request):
    mine = request.user
    orders = Order.objects.filter(user=mine, complete=False, cancelled=False).order_by('-id')
    fin = Order.objects.filter(user=mine, complete=True).order_by('-id')
    return render(request, 'frontmain/OrderListView.html', {'orders':orders, 'fin':fin})


@login_required
def OrderListViewComplete(request):
    mine = request.user
    orders = Order.objects.filter(user=mine, complete=True, cancelled=False).order_by('-id')
    return render(request, 'frontmain/OrderListViewComplete.html', {'orders':orders})

@login_required
def OrderListViewAll(request):
    mine = request.user
    orders = Order.objects.filter(user=mine).order_by('-id')
    return render(request, 'frontmain/OrderListViewAll.html', {'orders':orders})

def MakePayment(request, id):
    order = Order.objects.get(id=id)
    cost = order.pages * 300
    order_id = order.id
    print(cost)
    return render(request, 'frontmain/makePayment.html', {'cost':cost, 'order_id':order_id})

def createpayment(request):
    if request.method == 'POST':
        phonenumber = request.POST['phonenumber']
        cost = request.POST['price']
        ordernumber = request.POST['order_pk']
        phonenumber = request.POST['phonenumber']
        new_payment = TestModel(phonenumber=phonenumber, cost=cost, ordernumber=ordernumber)
        new_payment.save()
        return HttpResponse('successfully updated payment')
    

@login_required
@require_POST
def payment(request):
    cl = MpesaClient()
    if request.method == 'POST':
        phonenumber = request.POST['phonenumber']
        cost = int(request.POST['price'])
        ordernumber = request.POST['order_pk']
        phonenumber = str(request.POST['phonenumber'])
        user_id = request.user.id
        account_reference = 'reference'
        transaction_desc = 'Description'
        callback_url = 'https://kpsea.testprepken.com/billing/callback/{0}/{1}/'.format(user_id, ordernumber)
        #response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
        print(ordernumber)
        print(callback_url)
        print(account_reference)
        print(cost)
        print(phonenumber)
        # new_payment = TestModel(phonenumber=phonenumber, cost=cost, ordernumber=ordernumber)
        # new_payment.save()
        return HttpResponse('successfully updated payment')
    

def about(request):
    return render(request, 'frontmain/about.html')


@login_required
def OrderUpdate(request, id):
     order = Order.objects.get(id=id)
     if request.method == 'POST':
         form = OrderCreationForm(request.POST, instance=order)
         if form.is_valid():
             form.save()
             return redirect('order_detail', order.id) 
     else:
         form = OrderCreationForm(instance=order)
     return render(request, 'frontmain/newOrder.html',  {'form': form})


def payCallback(request, id):
    order = Order.objects.get(id=id)
    time_now = datetime.now(timezone.utc)
    order.time_paid = time_now
    order.paid = True
    if order.days and order.hours:
        order.deadline = time_now + timedelta(days=order.days, hours=order.hours)
    elif order.days and not order.hours:
        order.deadline = time_now + timedelta(days=order.days)
    elif order.hours and not order.days:
        order.deadline = time_now + timedelta(hours=order.hours)
    order.save()
    return redirect('home')


@login_required
def orderDetailModView(request, id):
    order = Order.objects.get(id=id)
    form = ModMessagesForm()
    orderinfo = OrderData.objects.filter(order=order)
    if order.time_paid:
        if order.days and order.hours:
            deadline = order.time_paid + timedelta(days=order.days, hours=order.hours)
        elif order.days and not order.hours:
            deadline = order.time_paid + timedelta(days=order.days)
        elif order.hours and not order.days:
            deadline = order.time_paid + timedelta(hours=order.hours)
    else:
        deadline = None

    cost = order.pages * 300
    words = order.pages * 275
    if request.method == "POST":
        form = ModMessagesForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.order = order
            obj.is_mod = True
            if obj.is_answer == True:
                order.complete = True
                order.save()
            obj.save()
            return redirect('order_detail', order.id)
        else:
            form = ModMessagesForm()
    return render(request, 'frontmain/OrderDetail.html', {
        'order':order, 
        'form':form, 
        # 'time_left':time_left,
        # 'time_left1':time_left1, 
        'orderinfo':orderinfo, 
        'cost':cost, 
        'words':words, 
        'deadline':deadline
        })


@login_required
def CancelOrder(request):
    mine = request.user
    orders = Order.objects.filter(user=mine, complete=False, cancelled=False, paid=True).order_by('-id')
    return render(request, 'frontmain/OrderCancelView.html', {'orders':orders})

@login_required
def Cancel(request, id):
    order = Order.objects.get(id=id)
    order.cancelled = True
    order.save()
    messages.success(request, f'Order cancelled successfully')
    return redirect('home')

