from django.urls import path
from django.contrib.auth.views import (LoginView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)

from app import views
from .forms import (LoginForm,
                    ChangePasswordForm,
                    ResetPasswordForm,
                    MySetPasswordForm)
urlpatterns = [
    path('', views.ProductView.as_view(),name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('electronics/', views.electronics, name='electronics'),
    path('electronics/<slug:data>', views.electronics, name='data'),
#------------------------- Cart Section----------------------------------------------------
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart_quantity/', views.cart_quantity, name='cart_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path('buy/', views.buy_now, name='buy-now'),
#------------------------- Address Section----------------------------------------------------
    path('address-list/', views.addressList, name='address_list'),
    path('address/', views.address, name='address'),
    path('edit-address/<int:pk>', views.editAddress, name='edit-address'),
    path('delete-address/<int:pk>', views.deleteAddress, name='delete-address'),


#------------------------- Register, Login, Logout Section---------------------------------------
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('login/', LoginView.as_view(template_name='app/login.html',form_class=LoginForm), name='login'),
    path('logout/', views.signout, name='logout'),
    path('registration/', views.customerregistration, name='customerregistration'),
#   if we don't provide success_url in 'PasswordChangeView'. We'll get an error for reverse url for 'change_password_done' url.
    path('changepassword/', PasswordChangeView.as_view(form_class=ChangePasswordForm,template_name='app/changepassword.html',success_url='/profile/'), name='changepassword'),

    path('password_reset/', PasswordResetView.as_view(form_class=ResetPasswordForm,template_name='app/passwordReset.html',), name='password-reset'),

    path('password_reset_done/', PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm), name='password_reset_confirm'),

    path('password_reset_complete/', PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

]
