from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.urls import path

from accounts import views
from accounts.forms import EmailAuthenticationForm
from .views import AuthRegister, AuthInfoUpdateView, AuthInfoGetView
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(form_class=EmailAuthenticationForm, template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # RestApi
    path('user_register/', AuthRegister.as_view()),
    path('user_update/', AuthInfoUpdateView.as_view()),
    path('mypage/', AuthInfoGetView.as_view()),
    # jwtトークン取得
    path("get_token/", obtain_jwt_token),
]
