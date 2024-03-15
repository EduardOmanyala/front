from django.db import models
from custom_user.models import User
from frontmain.models import Order
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage, send_mail

# Create your models here.
class PayData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    #amount = models.CharField(max_length=500)
    created_at =  models.DateTimeField(auto_now_add=True)
    phonenumber = models.TextField(null=True, blank=True)
    transcode = models.TextField(null=True, blank=True)
    class Meta:
        verbose_name_plural = 'Paydata'


# def create_payment(sender, instance, created, **kwargs):
#     if created:
#         #handler = User.objects.filter(user=instance)
#         print(instance.user)
#         email = str(instance.user)
#         html_template = 'billing/billingsucces.html'
#         html_message = render_to_string(html_template)
#         subject = 'We are working on your paper!'
#         email_from = 'Testprep@testprepken.com'
#         recipient_list = [email]
#         message = EmailMessage(subject, html_message, email_from, recipient_list)
#         message.content_subtype = 'html'
#         message.send(fail_silently=True)


# post_save.connect(create_payment, sender=PayData)


    
