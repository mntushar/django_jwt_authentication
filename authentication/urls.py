from django.urls import path

from backend.account.authentication.views import AsyncLoginView, AsyncAccessTokenView

urlpatterns = [
    path('login', AsyncLoginView.as_view(), name='login'),
    path('access-token/', AsyncAccessTokenView.as_view(), name='access_token_view'),
]