from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



urlpatterns =[
    path('',views.dashboard,name='dashboard'),
    path('register/',views.registerPage,name='register_page'),
    path('login/',views.loginPage,name='login_page'),
    path('logout/',views.logoutPage,name='logout_page'),
    path('userPage/',views.userPage,name='user_page'),
    path('accountSettings/',views.accountSettings,name='account_settings'),
    
    path('products/',views.products,name='products'),
    path('customers/<str:pk>/',views.customers,name='customers'),
    path('created_order/<str:pk>/',views.createOrder,name='create_order'),
    path('update_order/<str:pk>/',views.updateOrder,name='update_order'),
    path('delete_order/<str:pk>/',views.deleteOrder,name='delete_order'),

    path('createproduct/',views.createProduct,name='createproduct'),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),name="password_reset_complete"),
    
    ]

'''
1 - submit email form                     //PasswordResetView.as_view()
2 - Email sent success message            //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email   //PasswordResetConfirmView.as_view()
4 - Password successFully changed message //PasswordResetCompleteView.as_view() 
'''
