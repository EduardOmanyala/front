from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django_daraja.mpesa.core import MpesaClient
from django.views.decorators.csrf import csrf_exempt
import json
from frontmain.models import Order
from billing.models import PayData
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from custom_user.models import User
from .forms import UserRegisterForm
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from datetime import timedelta

from datetime import datetime, timezone

# Create your views here.


@login_required
def mpesarequest(request):
    cl = MpesaClient()
    #get user details
    #mydata = Post.objects.filter(user=request.user).order_by('-id')[:1]
    #phone_number = mydata[0]
    #print(phone_number)
    user_id = request.user.id
    #print(user_id)
    phone_number = '0717895728'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://kpsea.testprepken.com/billing/callback/1/'
    #callback_url = 'https://kpsea.testprepken.com/billing/callback/{0}/'.format(user_id)
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)


@login_required
def Proceed2Payment(request, id):
    order = Order.objects.get(id=id)
    cost = order.pages * 300
    order_id = order.id
    print(cost)
    return render(request, 'billing/payment.html', {'cost':cost, 'order_id':order_id})

@login_required
def PaymentEmail(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.title:
        title = 'Untitled'
    else:
        title = order.subject
    subject = order.subject
    email = str(request.user.email)
    html_template = 'billing/billingsucces.html'
    html_message = render_to_string(html_template, {'title': title, 'subject': subject})
    subject = 'We Are Working On Your Paper!'
    email_from = 'Testprep@testprepken.com'
    recipient_list = [email]
    message = EmailMessage(subject, html_message, email_from, recipient_list)
    message.content_subtype = 'html'
    message.send(fail_silently=True)
    return redirect('home') 










@login_required
def payment(request):
    cl = MpesaClient()
    if request.method == 'POST':
        amount = int(request.POST['price'])
        ordernumber = request.POST['order_pk']
        phonenumber = str(request.POST['phonenumber'])
        user_id = request.user.id
        account_reference = 'reference'
        transaction_desc = 'Description'
        callback_url = 'https://kpsea.testprepken.com/billing/callback/{0}/{1}/'.format(user_id, ordernumber)
        response = cl.stk_push(phonenumber, amount, account_reference, transaction_desc, callback_url)
        # print(ordernumber)
        # print(callback_url)
        # print(account_reference)
        # print(amount)
        # print(phonenumber)
        # new_payment = TestModel(phonenumber=phonenumber, cost=cost, ordernumber=ordernumber)
        # new_payment.save()
        return HttpResponse(response)
    


@csrf_exempt
def callbackurl(request, id, ord_id):
    user_id = User.objects.get(id=id)
    order = Order.objects.get(id=ord_id)
    if request.method == 'POST':
        m_body =request.body.decode('utf-8')
        mpesa_payment = json.loads(m_body)
        payment = PayData(
            phonenumber=mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value'],
        	transcode=mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value'],
            user=user_id,
            order=order
        )
        payment.save()
        order.time_paid = datetime.now(timezone.utc)
        order.paid = True
        order.save()
        context = {
             "ResultCode": 0,
             "ResultDesc": "Accepted"
        }
        return JsonResponse(dict(context))
    

def getPayment(request, id):
    order = Order.objects.get(id=id)
    #info = PayData.objects.filter(order=order)
    if order.paid == True:
        data = {'message': 'Hello, World!'}
        return JsonResponse(data)
    # order = Order.objects.get(id=id)
    # data = {'success': False} 
    # info = Payments.objects.filter(order=order)
    # print(info)
    # if info:
    #     data['success'] = True
    #     return HttpResponse(data)




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account Created for {email}, you can now login')
            html_template = 'billing/welcomemail.html'
            html_message = render_to_string(html_template)
            subject = 'Welcome to Testprep!'
            email_from = 'Testprep@testprepken.com'
            recipient_list = [email]
            message = EmailMessage(subject, html_message,
                                   email_from, recipient_list)
            message.content_subtype = 'html'
            message.send(fail_silently=True)
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'billing/register.html', {'form':form})




def mailtest1(request):
    send_mail('Using SparkPost with Django123', 'This is a message from Django using SparkPost!123', 'Testprep@testprepken.com',
    ['bestessays001@gmail.com'], fail_silently=True)
    return redirect('home')


