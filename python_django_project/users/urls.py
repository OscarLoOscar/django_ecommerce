from django.urls import path,reverse_lazy
# reverse_lazy 會「等到真係要navigate時」自去搵網址
# success_url 係 「任務成功後的目的地」
from  . import views
from django.contrib.auth import views as auth_views
app_name = 'users' 

urlpatterns = [
  path('signin/',views.login,name = 'signin'),
  path('logout/',views.logout,name='logout'),
  path('register/',views.register,name='register'),
  path('dashboard/',views.dashboard,name='dashboard'),
  # forget password
  path('password/new/',
        auth_views.PasswordResetView.as_view(
          template_name='users/forget_password.html',
          email_template_name='users/password_reset_email.txt', # add this line for replace 'password_reset_confirm' to 'users:password_reset_confirm'
          success_url=reverse_lazy('users:password_reset_done')),
          name='password_reset'),
  path('password/sent/',auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_email_done.html'),name="password_reset_done"),
  path('password/reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',success_url=reverse_lazy('users:password_reset_complete')),name="password_reset_confirm"),
  path('password/success/',auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name="password_reset_complete"),
]