from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from billing import views as bill_views

urlpatterns = [
    path('payments', bill_views.payment, name='payment'),
    path('order/details/payment/<int:id>/', bill_views.Proceed2Payment, name='proceed_payment'),
    path('getpayment/<int:id>/', bill_views.getPayment, name='get_payment'),
    path('payment/complete/<int:order_id>/', bill_views.PaymentEmail, name='payment-complete'),
    path('payment/callback/<int:id>/<int:ord_id>/', bill_views.callbackurl, name='callback_payment'),
    path('mpesa/request/', bill_views.mpesarequest, name='mpesa_payment'),
    path('login/', auth_views.LoginView.as_view(template_name='billing/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path('register/', bill_views.register, name='register'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='billing/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="billing/reset_password_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="billing/password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="billing/password_reset_done.html"), name='password_reset_complete'),
    path('test1/', bill_views.mailtest1, name='mailtest'),


]