"""
Connect method docstring: Brief description of the connect method.
"""
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

from django.conf import settings
from django.core.mail import send_mail

from .models import NewsLetterUsers
from .serializer import ContactFormSerializer, NewsLetterUsersSerializer


# Create your views here.


class ContactFormView(generics.CreateAPIView):
    """
    Connect method docstring: Brief description of the connect method.
    """
    permission_classes = [AllowAny]
    queryset = None
    serializer_class = ContactFormSerializer

    def post(self, request):
        """
        Connect method docstring: Brief description of the connect method.
        """
        serializer = ContactFormSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']

            try:
                send_mail(
                    subject,
                    message,
                    email,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                return Response({'message': 'Mail sent successfully'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'message': 'Failed to send email', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # return Response({'message': 'Data submitted successfully'}, status=status.HTTP_201_CREATED)


# client = MailchimpMarketing.Client()
# client.set_config({
#     "api_key": settings.MAILCHIMP_API_KEY,
#     "server": settings.MAILCHIMP_REGION
# })


class NewsLetterUsersAPI(generics.CreateAPIView):
    """
    Connect method docstring: Brief description of the connect method.
    """
    permission_classes = [AllowAny]
    queryset = NewsLetterUsers.objects.all()
    serializer_class = NewsLetterUsersSerializer

    def post(self, request):
        """
        Connect method docstring: Brief description of the connect method.
        """
        # email = request.data.get('email')
        # member_info = {
        #     'email_address': email,
        #     'status': 'subscribed',
        # }

        serializer = NewsLetterUsersSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):

            email = serializer.validated_data['email']
            email_newsletter = NewsLetterUsers.objects.create(email=email)

            print(email_newsletter)

        return Response({'message': 'Data submitted successfully'}, status=status.HTTP_200_OK)

        # try:
        #     response = client.lists.add_list_member(
        #         settings.MAILCHIMP_MARKETING_AUDIENCE_ID, member_info)

        #     print(response)
        #     return Response(status=status.HTTP_200_OK)

        # except ApiClientError as error:
        #     print("Error: {}".format(error.text))
        #     return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        all_emails = NewsLetterUsers.objects.all()

        # format of each object is <email: njewqjehq2@njhew.com"> required is email only w/o the keyword 'email'
        email_addresses = [user.email for user in all_emails]

        print(email_addresses)

        subject = 'A New Post!'
        message = 'we added a new post! Head down to our website to read the full blog.'
        from_email = settings.EMAIL_HOST_USER

        # for email in email_addresses:
        send_mail(
            subject,
            message,
            from_email,
            email_addresses,
            # [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return Response({'message': 'Data submitted successfully'}, status=status.HTTP_200_OK)
