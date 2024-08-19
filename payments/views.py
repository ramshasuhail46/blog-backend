"""
Connect method docstring: Brief description of the connect method.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

import stripe

from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessAPI(APIView):
    """
    Connect method docstring: Brief description of the connect method.
    """

    def get(self, request):
        """
    Connect method docstring: Brief description of the connect method.
    """
        user = request.user
        if user.is_authenticated:
            if not user.is_pro:
                user.is_pro = True
                user.save()

        return Response({
            'status': status.HTTP_202_ACCEPTED,
            'message': 'Transaction completed'
        })


class CancelAPI(APIView):
    """
    Connect method docstring: Brief description of the connect method.
    """

    def get(self):
        """
        Connect method docstring: Brief description of the connect method.
        """
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Transaction Failed'
        })


class CheckoutAPI(APIView):
    """
    Connect method docstring: Brief description of the connect method.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Connect method docstring: Brief description of the connect method.
        """
        try:
            domain = 'http://127.0.0.1:8000/payment/'

            checkout_session = stripe.checkout.Session.create(
                mode="subscription",
                payment_method_types=["card"],
                line_items=[
                    {"price": "price_1Ovu1RFlw1Z8BLlbRssq8iiC", "quantity": 1}
                ],
                success_url='http://localhost:3000/',
                cancel_url='http://localhost:3000/checkout/',
            )

            user = request.user
            user.is_pro = True
            user.save()

            return Response(
                {
                    'status': status.HTTP_202_ACCEPTED,
                    'message': 'Transaction completed',
                    'id': checkout_session
                }
            )
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
