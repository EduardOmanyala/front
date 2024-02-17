from django import forms
from django.forms import ClearableFileInput

from frontmain.models import Order, OrderData



class OrderCreationForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['title','subject', 'pages', 'hours', 'days' ]


class OrderDetailsForm(forms.ModelForm):
    class Meta:
        model = OrderData
        fields = ['instructions','file']


class ModMessagesForm(forms.ModelForm):
    class Meta:
        model = OrderData
        fields = ['instructions','file', 'is_answer']


