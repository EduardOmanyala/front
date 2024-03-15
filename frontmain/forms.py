from django import forms
from django.forms import ClearableFileInput

from frontmain.models import Order, OrderData



class OrderCreationForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['title','subject', 'level', 'pages', 'hours', 'days' ]


class OrderDetailsForm(forms.ModelForm):
    class Meta:
        model = OrderData
        fields = ['instructions', 'file']


class ModMessagesForm(forms.ModelForm):
    class Meta:
        model = OrderData
        fields = ['instructions','file', 'is_answer']




class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class LimitedMultipleField(forms.FileField):
    def __init__(self, max_files=5, max_file_size=10 * 1024 * 1024, *args, **kwargs):
        self.max_files = max_files
        self.max_file_size = max_file_size
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            if len(data) > self.max_files:
                raise forms.ValidationError(f'You can upload up to {self.max_files} files only.')
            result = [single_file_clean(d, initial) for d in data]
            for file in result:
                if file.size > self.max_file_size:
                    raise forms.ValidationError(f'File size should not exceeed {self.max_file_size} bytes')
        else:
            result = single_file_clean(data, initial)
        return result
    

class FileOrderDetailsForm(forms.ModelForm):
    class Meta:
        model = OrderData
        fields = ['file']
    file = LimitedMultipleField()
