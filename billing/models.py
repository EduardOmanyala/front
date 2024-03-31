from django.db import models
from custom_user.models import User
from frontmain.models import Order
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from tinymce.models import HTMLField
import os

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


    
    
class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = HTMLField(blank=True, null=True)
    file = models.FileField(upload_to='contactFiles/', blank=True, null=True)
    created_at =  models.DateTimeField(auto_now_add=True)


    @property
    def filename(self):
        return os.path.basename(self.file.name)

    @property
    def css_class(self):
        name, extension = os.path.splitext(self.file.name)
        if extension == '.pdf':
            return 'fa-file-pdf-o'
        elif extension == '.docx':
            return 'fa-file-word-o'
        elif extension == '.doc':
            return 'fa-file-word-o'
        elif extension == '.xlsx':
            return 'fa-file-excel-o'
        else:
            return 'fa-file-text-o'   
        



class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = HTMLField(blank=True, null=True)
    img = models.ImageField(upload_to='blogFiles/', blank=True, null=True)
    created_at =  models.DateTimeField(auto_now_add=True)
