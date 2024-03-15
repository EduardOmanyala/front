from django.urls import path, reverse_lazy

from frontmain import views as front_views

urlpatterns = [
    path('', front_views.dash, name='home'),
    path('sample', front_views.homepage, name='samples'),
    path('extends', front_views.extender, name='ext'),
    path('orders/create', front_views.createOrder, name='create'),
    path('orders/create/new', front_views.newOrder, name='create_new'),
    path('orders/dashboard', front_views.OrderListView, name='order-list-view'),
    path('orders/dashboard/complete', front_views.OrderListViewComplete, name='order-list-view-complete'),
     path('orders/dashboard/all', front_views.OrderListViewAll, name='order-list-view-all'),
    path('orders/cancel', front_views.CancelOrder, name='order-cancel-view'),
    path('order/details/<int:id>/', front_views.OrderDetail, name='order_detail'),
    path('order/files/details/<int:id>/', front_views.FileUploadView, name='order_files'),
    path('mods/order/details/<int:id>/', front_views.orderDetailModView, name='order_detail_mod'),
    path('order/details/messages/<int:id>/', front_views.OrderMessagesNotification, name='order_emails_messages_send'),
    path('order/details/messages/<int:id>/', front_views.OrderMessagesNotificationBrowser, name='order_emails_messages'),
    path('order/payment/<int:id>/', front_views.MakePayment, name='order_payment'),
    path('update/order/<int:id>/', front_views.OrderUpdate, name='order_update'),
    path('order/callback/<int:id>/', front_views.payCallback, name='order_payment_callback'),
    path('create', front_views.payment, name='create_payment'),
    path('about', front_views.about, name='about'),
    path('cancel/order/<int:id>/', front_views.Cancel, name='cancel_success'),

]
