from django.db import models
from custom_user.models import User
from frontmain.models import Order

# Create your models here.
class PayData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.CharField(max_length=500)
    created_at =  models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Paydata'

    def __str__(self):
        return self.amount