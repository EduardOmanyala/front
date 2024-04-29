from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django_daraja.mpesa.core import MpesaClient
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import base64
from frontmain.models import Order
from billing.models import PayData, Contact, BlogPost
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from custom_user.models import User
from .forms import UserRegisterForm, ContactUsForm, BlogPostForm
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from datetime import timedelta
import random

from datetime import datetime, timezone
from front.settings import MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET, MPESA_PASSKEY, MPESA_SHORTCODE

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
    cost = order.pages * 1
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
    subject_diff = str((random.randint(1, 1000000000)))
    email = str(request.user.email)
    html_template = 'billing/billingsucces.html'
    html_message = render_to_string(html_template, {'title': title, 'subject': subject})
    subject = 'We Are Working On Your Paper! - {0}'.format(subject_diff)
    email_from = 'Ace@testprepken.com'
    recipient_list = [email]
    message = EmailMessage(subject, html_message, email_from, recipient_list)
    message.content_subtype = 'html'
    message.send(fail_silently=True)
    return redirect('home') 



@login_required
def PaymentRedirectEmail(request, id):
    order = Order.objects.get(id=id)
    return redirect('payment-complete', order.id) 








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
        callback_url = 'https://ace-stars.com/payment/callback/{0}/{1}/'.format(user_id, ordernumber)
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
            subject = 'Welcome to Ace-Stars!'
            email_from = 'Ace@testprepken.com'
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
    send_mail('AsdsUsing SparkPost with Django123', 'This is a message from Django using email', 'no-reply@ace-stars.com',
    ['bestessays001@gmail.com'], fail_silently=True)
    return redirect('home')

@login_required
def ContactUsView(request):
    me = request.user
    myMessages = Contact.objects.filter(user=me).order_by('-id')[:15]
    form = ContactUsForm()
    if request.method == "POST":
            form = ContactUsForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = me
                obj.save()
                return redirect('contact-us-notification', me.id)
            else:
                form = ContactUsForm()
    return render(request, 'billing/ContactUs.html', {'myMessages':myMessages, 'form':form})


@login_required
def ContactNotification(request, id):
    me = User.objects.get(id=id)
    #email = str(request.user.email)
    email = 'bestessays001@gmail.com'
    subject_diff = str((random.randint(1, 1000000000)))
    html_template = 'billing/contactMessages.html'
    html_message = render_to_string(html_template)
    subject = 'New Message from User {0} - {1}'.format(me.id, subject_diff)
    email_from = 'Ace@testprepken.com'
    recipient_list = [email]
    message = EmailMessage(subject, html_message, email_from, recipient_list)
    message.content_subtype = 'html'
    message.send(fail_silently=True)
    reply = Contact(
            user=me,
        	text='We have received your message. We will contact you shortly by mail or phone. Best Regards'

        )
    reply.save()
    return redirect('contact-us-view')



@login_required
def BlogPostCreateView(request):
    form = BlogPostForm()
    if request.method == "POST":
            form = BlogPostForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
                return redirect('post-detail', obj.id)
            else:
                form = BlogPostForm()
    return render(request, 'billing/BlogpostCreate.html', {'form':form})




def BlogPostListView(request):
    posts = BlogPost.objects.all().order_by('-id')[:15]
    return render(request, 'billing/BlogListView.html', {'posts':posts})


def BlogPostDetailView(request, id):
    post = BlogPost.objects.get(id=id)
    return render(request, 'billing/BlogDetailView.html', {'post':post})



#mpesa

def get_access_token(request):
    access_token_url = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    headers = {'Content-Type': 'application/json'}
    auth = (MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET)
    try:
        response = requests.get(access_token_url, headers=headers, auth=auth)
        response.raise_for_status() 
        result = response.json()
        access_token = result['access_token']
        return JsonResponse({'access_token': access_token})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)})
    



def format_phone_number(phone_number):
	return '254' + phone_number[-9:]


def initiate_stk_push(request):
    if request.method == 'POST':
        amount_val = int(request.POST['price'])
        ordernumber = request.POST['order_pk']
        phonenumber_pay = str(request.POST['phonenumber'])
        number_pay = '254' + phonenumber_pay[-9:]
        user_id = request.user.id
        account_reference = 'reference'
        transaction_desc = 'Description'
        #callback_url_order = 'https://ace-stars.com/payment/callback/{0}/{1}/'.format(user_id, ordernumber)
        access_token_response = get_access_token(request)
        if isinstance(access_token_response, JsonResponse):
            access_token = access_token_response.content.decode('utf-8')
            access_token_json = json.loads(access_token)
            access_token = access_token_json.get('access_token')
            if access_token:
                amount = amount_val
                phone = number_pay
                process_request_url = 'https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
                callback_url = 'https://ace-stars.com/payment/callback/{0}/{1}/'.format(user_id, ordernumber)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                password = base64.b64encode((MPESA_SHORTCODE + MPESA_PASSKEY + timestamp).encode()).decode()
                party_a = phone
                party_b = ''
                account_reference = 'Order 79654{0}'.format(ordernumber)
                transaction_desc = 'stkpush test'
                stk_push_headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + access_token
                }
                
                stk_push_payload = {
                    'BusinessShortCode': MPESA_SHORTCODE,
                    'Password': password,
                    'Timestamp': timestamp,
                    'TransactionType': 'CustomerPayBillOnline',
                    'Amount': amount,
                    'PartyA': party_a,
                    'PartyB': MPESA_SHORTCODE,
                    'PhoneNumber': party_a,
                    'CallBackURL': callback_url,
                    'AccountReference': account_reference,
                    'TransactionDesc': transaction_desc
                }

                try:
                    response = requests.post(process_request_url, headers=stk_push_headers, json=stk_push_payload)
                    response.raise_for_status()   
                    # Raise exception for non-2xx status codes
                    response_data = response.json()
                    checkout_request_id = response_data['CheckoutRequestID']
                    response_code = response_data['ResponseCode']
                    
                    if response_code == "0":
                        return JsonResponse({'CheckoutRequestID': checkout_request_id, 'ResponseCode': response_code})
                    else:
                        return JsonResponse({'error': 'STK push failed.'})
                except requests.exceptions.RequestException as e:
                    return JsonResponse({'error': str(e)})
            else:
                return JsonResponse({'error': 'Access token not found.'})
        else:
            return JsonResponse({'error': 'Failed to retrieve access token.'})
        


    
def Profile(request):
    all = Order.objects.filter(user=request.user).count()
    complete = Order.objects.filter(user=request.user, complete=True).count()
    current = Order.objects.filter(user=request.user, complete=False).count()
    return render(request, 'billing/profile.html', {'all':all, 'complete':complete, 'current':current})
