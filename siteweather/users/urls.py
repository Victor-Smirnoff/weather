from django.contrib.auth.views import LogoutView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy
from . import views

app_name = 'users'

urlpatterns = [
    path(route='login/', view=views.LoginUser.as_view(), name='login'),
    path(route='logout/', view=LogoutView.as_view(), name='logout'),
    path(route='register/', view=views.RegisterUser.as_view(), name='register'),
    path(route='profile/', view=views.ProfileUser.as_view(), name='profile'),
    path(route='password-change/', view=views.UserPasswordChange.as_view(), name='password_change'),
    path(route='password-change/done/',
         view=PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'
    ),
    path(route='password-reset/',
         view=PasswordResetView.as_view(template_name='users/password_reset_form.html',
                                        email_template_name='users/password_reset_email.html',
                                        success_url=reverse_lazy('users:password_reset_done')
                                        ),
         name='password_reset'
         ),
    path(route='password-reset/done/',
         view=PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'
         ),
    path(route='password-reset/<uidb64>/<token>/',
         view=PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                                success_url=reverse_lazy('users:password_reset_complete')
                                               ),
         name='password_reset_confirm'
         ),
    path(route='password-reset/complete/',
         view=PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'
         ),
]