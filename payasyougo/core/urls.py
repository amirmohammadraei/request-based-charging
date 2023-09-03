from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('token/', UserTokenCreateView.as_view(), name='user-token-create'),
    path('create-request/', RequestCreateView.as_view(), name='create-request'),
    path('request-list/', RequestListView.as_view(), name='request-list'),
    path('calculate-total-price/', TotalPriceView.as_view(), name='calculate-total-price'),
    path('current-month-cost/', CurrentMonthCostView.as_view(), name='current-month-cost'),
]
