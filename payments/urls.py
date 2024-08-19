"""
Connect method docstring: Brief description of the connect method.
"""
from django.urls import path

from .views import CheckoutAPI, SuccessAPI, CancelAPI

APP_NAME = 'payments'

urlpatterns = [
    path('', CheckoutAPI.as_view(), name='checkout'),
    path('success/', SuccessAPI.as_view(), name='success'),
    path('cancel/', CancelAPI.as_view(), name='cancel')
]
