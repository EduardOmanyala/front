from django.db import models
from custom_user.models import User
from tinymce.models import HTMLField
from django import forms
import os
from datetime import timedelta
from datetime import datetime, timezone

# Create your models here.
LEVEL_CHOICES = (
    ('High School','High School'),
    ('College', 'College'),
    ('Masters','Masters'),
    ('PhD', 'PhD'),
)

SUBJECT_CHOICES = (
    ('Accounting','Accounting'),
    ('Management', 'Management'),
    ('Nursing','Nursing'),
    ('English', 'English'),
    ('Marketing','Marketing'),
    ('Art', 'Art'),
    ('History','History'),
    ('Law', 'Law'),
    ('Economics','Economics'),
    ('Writing', 'Writing'),
)

TYPE_CHOICES = (
    ('1','1'),
    ('2', '2'),
    ('3','3'),
    ('4', '4'),
    ('5','5'),
    ('6', '6'),
    ('7','7'),
    ('8', '8'),
    ('9','9'),
    ('10', '10'),
)

HOUR_CHOICES = (
    ('0','0'),
    ('6', '6'),
    ('7','7'),
    ('8', '8'),
    ('9','9'),
    ('10', '10'),
)

DAY_CHOICES = (
    ('0','0'),
    ('1','1'),
    ('2', '2'),
    ('3','3'),
    ('4', '4'),
    ('5','5'),
    ('6', '6'),
    ('7','7'),
    ('8', '8'),
    ('9','9'),
    ('10', '10'),
)

# def file_size(value):
#     limit = 10 * 1024 * 1024

#     if isinstance(value, (list, tuple)):
#         for file in value:
#             if file.size > limit:
#                 raise forms.ValidationError('Files size should not exceed 10 MB.')
#             else:
#                 if value.size > limit:
#                     raise forms.ValidationError('Files size should not exceed 10 MB.')







class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=500, blank=True, null=True, choices=SUBJECT_CHOICES, default='Accounting')
    level = models.CharField(max_length=500, blank=True, null=True, choices=LEVEL_CHOICES, default='College')
    pages = models.IntegerField(default=1)
    hours = models.IntegerField(blank=True, null=True)
    days = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    time_paid = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)


    @property
    def deadline(self):
        if self.paid == True:
            if self.days and self.hours:
                deadline = self.time_paid + timedelta(days=self.days, hours=self.hours)
            elif self.days and not self.hours:
                deadline = self.time_paid + timedelta(days=self.days)
            elif self.hours and not self.days:
                deadline = self.time_paid + timedelta(hours=self.hours)
        else:
            deadline = None
        return deadline
    
    @property
    def time_left(self):
        if self.paid == True:
            if self.days and self.hours:
                deadline = self.time_paid + timedelta(days=self.days, hours=self.hours)
            elif self.days and not self.hours:
                deadline = self.time_paid + timedelta(days=self.days)
            elif self.hours and not self.days:
                deadline = self.time_paid + timedelta(hours=self.hours)
        else:
            deadline = None
        if deadline != None:
            #time_balance = deadline - datetime.now(timezone.utc)
            if deadline > datetime.now(timezone.utc):
                time_left = str(deadline - datetime.now(timezone.utc))[:-10]
            else:
                time_left = "None"
        else:
            time_left = None
        return time_left

    class Meta:
        verbose_name_plural = 'Orders'


    
class OrderData(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    instructions = HTMLField(blank=True, null=True)
    file = models.FileField(upload_to='1/', blank=True, null=True)
    created_at =  models.DateTimeField(auto_now_add=True)
    is_mod = models.BooleanField(default=False)
    is_answer = models.BooleanField(default=False)

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



    

class PayInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.CharField(max_length=500)
    created_at =  models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Payments'

    def __str__(self):
        return self.amount
    





class Moderators(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = 'Moderators'

    def __str__(self):
        return self.status
    

class TestModel(models.Model):
    phonenumber = models.CharField(max_length=500)
    cost = models.CharField(max_length=500)
    ordernumber = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = 'TestModel'

    



