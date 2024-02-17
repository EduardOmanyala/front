from django.contrib import admin

from frontmain.models import Order, OrderData, PayInfo, Moderators, TestModel

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderData)
admin.site.register(PayInfo)
admin.site.register(Moderators)
admin.site.register(TestModel)
