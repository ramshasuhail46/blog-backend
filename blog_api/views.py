"""
Connect method docstring: Brief description of the connect method.
"""
from rest_framework .views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, DjangoObjectPermissions, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import FileUploadParser,  MultiPartParser, FormParser

from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.models import Group, User
from django.contrib.gis.geoip2 import GeoIP2
from django.core.files.base import ContentFile

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from twilio.rest import Client

import json
import requests
import pandas as pd
import csv
from io import BytesIO, TextIOWrapper, StringIO
import io
from PIL import Image

from .serializer import (
    UserRegisterSerializer,
    UserLoginSerializer,
    PostSerializer,
    CommentSerializer,
    PostDetailSerializer,
    CommentDetailSerializer,
    CategorySerializer,
    Otpserializer,
    PredictionSerializer,
    ReplySerializer,
    EcommerceSerializer,
    VerifyAccountSerializer,
    CurrentUserSerializer,
    CartCheckoutSerializer,
    UserAddressSerializer,
    FileSerializer)
from .models import Post, Comment, Category, Notifications, Like, FileUploader, UserAddress, Cart, Ecommerce
from .ml_model import Model
from .email_otp import send_otp_via_email


User = get_user_model()


# Create your views here.


def get_tokens_for_user(user):
    """
    Connect method docstring: Brief description of the connect method.
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationAPI(APIView):
    """
    Connect method docstring: Brief description of the connect method.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Connect method docstring: Brief description of the connect method.
        """
        return Response({"message": "Register!"}, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Connect method docstring: Brief description of the connect method.
        """
        serializer = UserRegisterSerializer(data=request.data)
        recaptcha_response = request.data.get('g-recaptcha-response')

        if serializer.is_valid():

            user = serializer.save()

            send_otp_via_email(serializer.data['email'])

            payload = {
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }

            timeout = 20
            response = requests.post(
                'https://www.google.com/recaptcha/api/siteverify', data=payload, timeout=timeout)

            result = response.json()

            if not result['success']:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

            if user.is_creator:

                group = Group.objects.get(name='creator')
                user.groups.add(group)

                content = {
                    'data': serializer.data,
                    'message': 'Successfully Registered'
                }
                return Response(content, status=status.HTTP_201_CREATED)

            if user.is_editor:

                group = Group.objects.get(name='editor')
                user.groups.add(group)

                content = {
                    'data': serializer.data,
                    'message': 'Successfully Registered'
                }
                return Response(content, status=status.HTTP_201_CREATED)
            return Response({'msg': 'created!'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentPostPermission(DjangoObjectPermissions):
    """
    Connect method docstring: Brief description of the connect method.
    """
    message = "You do not have permission to perform this action."

    def has_object_permission(self, request, view, obj):
        """
        Connect method docstring: Brief description of the connect method.
        """
        if request.method in ['GET', 'POST', 'PUT']:
            return (
                request.user.has_perm('blog_api.add_post') or
                request.user.has_perm('blog_api.change_post')
            )
        else:
            return False


class UserLoginAPI(APIView):
    """
    Connect method docstring: Brief description of the connect method.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Connect method docstring: Brief description of the connect method.
        """
        return Response({'msg': 'Login please'}, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Connect method docstring: Brief description of the connect method.
        """
        serializer = UserLoginSerializer(data=request.data)
        recaptcha_response = request.data.get('g-recaptcha-response')
        print(request.data)
        if serializer.is_valid():

            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)

            if user is not None:

                payload = {
                    'secret': settings.RECAPTCHA_SECRET_KEY,
                    'response': recaptcha_response
                }

                timeout = 20
                response = requests.post(
                    'https://www.google.com/recaptcha/api/siteverify',
                    data=payload, timeout=timeout)

                result = response.json()
                # result['success'] = True

                if not result['success']:
                    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

                # print('here')
                token = get_tokens_for_user(user)
                print(token)
                return Response({'token': token, 'is_editor': user.is_editor, 'is_creator': user.is_creator}, status=status.HTTP_202_ACCEPTED)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        """
        Connect method docstring: Brief description of the connect method.
        """
        post = Post.postobjects.get(pk=pk)

        serializer = PostDetailSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryList(generics.ListCreateAPIView):
    """
    Connect method docstring: Brief description of the connect method.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostList(generics.ListCreateAPIView):
    """
    Connect method docstring: Brief description of the connect method.
    """
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    # queryset = Post.postobjects.all()

    def get_queryset(self):
        """
        Connect method docstring: Brief description of the connect method.
        """

        # logic for published/draft posting
        posts_to_draft = Post.objects.filter(
            status='published', to_be_posted__gt=timezone.now())
        posts_to_publish = Post.objects.filter(
            status='draft', to_be_posted__lte=timezone.now())

        posts_to_draft.update(status='Draft')
        posts_to_publish.update(status='Published')

        # logic for premium posts
        if self.request.user.is_authenticated:
            if not self.request.user.is_pro:
                posts = Post.postobjects.filter(is_post_pro=False)
            else:
                posts = Post.postobjects.all()
        else:
            # Assuming anonymous users can only view non-pro posts
            posts = Post.postobjects.filter(is_post_pro=False)

        return posts

    def perform_create(self, serializer):
        """
        Override perform_create to generate a thumbnail for a new post.
        """
        post = serializer.save()
        self.create_thumbnail(post)

    def create_thumbnail(self, post):
        """
        Generate a thumbnail for the given post.
        """
        if post.image:
            try:
                img = Image.open(post.image.path)
                img.thumbnail((500, 300))
                thumb_io = BytesIO()
                img.save(thumb_io, format='JPEG')
                thumb_content = ContentFile(
                    thumb_io.getvalue(), name=f'thumbnail_{post.image.name}')

                post.thumbnail.save(thumb_content.name,
                                    thumb_content, save=False)
                post.save()
            except Exception as e:
                print(f"Error generating thumbnail for post {post.title}: {e}")


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Connect method docstring: Brief description of the connect method.
    """

    # permission_classes = [CurrentPostPermission]
    serializer_class = PostDetailSerializer

    def get(self, request, *args, **kwargs):
        """
        Connect method docstring: Brief description of the connect method.
        """
        response = super().get(request, *args, **kwargs)
        self.update_post(self.get_object())
        return response

    def post(self, request, *args, **kwargs):
        pass

    def update_post(self, post):
        """
        Connect method docstring: Brief description of the connect method.
        """

        try:
            post_id = self.kwargs.get('pk')
            post = Post.postobjects.get(pk=post_id)

            # logic for setting is_trending to true
            comment_count = post.comments.count()
            if comment_count > 0 and post.likes > 5:
                post.is_trending = True

            # logic for setting is_popular to true
            if post.views > 5:
                post.is_popular = True

            post.save()

            return Response({'message': 'Post updated successfully'}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        """
        Connect method docstring: Brief description of the connect method.
        """

        posts_to_draft = Post.objects.filter(
            status='Published', to_be_posted__gt=timezone.now())
        posts_to_publish = Post.objects.filter(
            status='Draft', to_be_posted__lte=timezone.now())

        # posts_to_draft.update(status='Draft')
        # posts_to_publish.update(status='Published')

        for post in posts_to_draft:
            post.status = 'Draft'
            post.save()

        for post in posts_to_publish:
            post.status = 'Published'
            post.save()

        # self.update_post(instance)

        return Post.postobjects.all()


class CommentList(generics.ListCreateAPIView):
    """
    Connect method docstring: Brief description of the connect method.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        print(post_id)
        comments = Comment.objects.filter(post=post_id, parent=None)
        print(comments)
        return comments


class CommentDetail(generics.RetrieveUpdateAPIView):
    """
    Connect method docstring: Brief description of the connect method.
    """
    # permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()

    def get_serializer_context(self):
        """
        Connect method docstring: Brief description of the connect method.
        """
        context = super().get_serializer_context()
        context['pk'] = self.kwargs.get('pk')
        return context

    def post(self, request, *args, **kwargs):
        """
        Connect method docstring: Brief description of the connect method.
        """
        serializer = CommentDetailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            post_id = self.kwargs.get('pk')
            post = Post.postobjects.get(pk=post_id)

            serializer.context['pk'] = post_id

            parent = serializer.validated_data.get('parent', None)

            print("serializer: ", serializer.validated_data)
            print("parent: ", parent)

            if parent:
                serializer.validated_data['post'] = post_id
                serializer.validated_data['parent'] = parent
                serializer.save()

                message = 'Reply Added'
                user = request.user.email
                post_author = post.author.id

                send_notifications(request, user, message, post, post_author)

                # parent_comment = Comment.objects.get(id=parent)
                # serializer.validated_data['post'] = parent_comment.post
            else:
                serializer.validated_data['post'] = post_id
                serializer.save()

                message = 'Comment Added'
                user = request.user.email
                user_id = request.user
                post_author = post.author.id

                print("user_id", user_id)
                send_notifications(
                    request, user_id, message, post, post_author)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeView(APIView):
    """
    Connect method docstring: Brief description of the connect method.
    """
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     post_id = self.kwargs.get('pk')
    #     post = Post.postobjects.filter(pk=post_id)
    #     return Like.objects.filter(post=post)

    def post(self, request, pk):
        """
        Connect method docstring: Brief description of the connect method.
        """

        # likes_post = self.get_queryset()
        # like_count = likes_post.count()

        user_id = request.user
        post_id = self.kwargs.get('pk')
        post = Post.postobjects.get(pk=post_id)

        # post.likes += 1
        if Like.objects.filter(user=user_id, post=post).exists():
            return Response({'message': 'you cannot like a post twice!'}, status=status.HTTP_400_BAD_REQUEST)

        Like.objects.create(user=user_id, post=post)
        # post.save()

        liked_post = Like.objects.filter(post=post)
        like_count = liked_post.count()
        print("likes of post : ", like_count)

        message = 'Liked a post!'
        user = request.user.email
        post_author = post.author.id

        print("user_id", user_id)

        send_notifications(request, user_id, message, post, post_author)

        return Response({'postlikes': like_count}, status=status.HTTP_200_OK)

    def get(self, request, pk):

        post_id = self.kwargs.get('pk')
        post = Post.postobjects.get(pk=post_id)

        # post.likes += 1
        # Like.objects.create(user=user_id, post=post)
        # post.save()

        liked_post = Like.objects.filter(post=post)
        like_count = liked_post.count()
        print("likes of post : ", like_count)

        return Response({'postlikes': like_count}, status=status.HTTP_200_OK)


class View(APIView):
    """
    Connect method docstring: Brief description of the connect method.
    """
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        Connect method docstring: Brief description of the connect method.
        """
        post_id = self.kwargs.get('pk')
        print("postid: ", post_id)
        post = Post.postobjects.get(pk=post_id)
        post.views += 1
        post.save()

        return Response({'postviews': post.views},
                        status=status.HTTP_200_OK)


class CurrentUser(APIView):
    """
    Connect method docstring: Brief description of the connect method.
    """

    def get(self, request):
        """
        Connect method docstring: Brief description of the connect method.
        """
        if request.user.is_authenticated:
            email = request.user.email
            is_editor = request.user.is_editor
            is_creator = request.user.is_creator
            current_user_id = request.user.id
            return Response({'id': current_user_id, 'email': email, "is_editor": is_editor,
                            "is_creator": is_creator}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User Not Authenticated'}, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Connect method docstring: Brief description of the connect method.
        """
        serializer = CurrentUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            email = serializer.validated_data['email']
            user = User.objects.get(email=email)

            return Response({'id': user.id, 'email': user.email, "is_editor": user.is_editor,
                            "is_creator": user.is_creator, 'is_staff': user.is_staff}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User Not Authenticated'}, status=status.HTTP_200_OK)


def send_notifications(request, user, message, post, post_author):
    """
    Connect method docstring: Brief description of the connect method.
    """
    print("inside notification-s")

    channel_layer = get_channel_layer()

    # data = {'user': user,
    #         'message': message}

    # print(data)

    # id = request.user.id
    # print("id", id)
    print("post_author: ", post_author)

    room_group_name = f'user_{post_author}'
    print(f"Sending notification to room group: {room_group_name}")

    async_to_sync(channel_layer.send)(
        room_group_name,
        {
            'type': 'send_notification',
            'user':  user,
            'message': message,
            'post': post,
            'recipient_channel': room_group_name,
        }
    )
    return Response(status=status.HTTP_200_OK)


class SendOtp(APIView):
    """
    Connect method docstring: Brief description of the connect method.
    """

    def post(self, request):
        """
        Connect method docstring: Brief description of the connect method.
        """

        serializer = Otpserializer(data=request.data)
        if serializer.is_valid():

            user_id = serializer.validated_data["user_id"]
            phone_number = serializer.validated_data["number"]

            user = User.objects.get(id=user_id)
            user.phone_number = phone_number
            user.save()

            account_sid = settings.ACCOUNTSID
            auth_token = settings.AUTHTOKEN

            client = Client(account_sid, auth_token)

            verification = client.verify \
                .v2 \
                .services('VAa54620f320f6f11de5d346ce69537001') \
                .verifications \
                .create(to=phone_number, channel='sms')

            print(verification)

            return JsonResponse({'status': verification.status}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOtp(APIView):
    """
    Connect method docstring: Brief description of the connect method.
    """

    def post(self, request):
        """
        Connect method docstring: Brief description of the connect method.
        """
        serializer = Otpserializer(data=request.data)
        if serializer.is_valid():

            account_sid = settings.ACCOUNTSID
            auth_token = settings.AUTHTOKEN

            client = Client(account_sid, auth_token)

            verification_check = client.verify \
                .v2 \
                .services('VAa54620f320f6f11de5d346ce69537001') \
                .verification_checks \
                .create(to=request.data.phone_number, code=request.data.otp)

            if verification_check.status == 'approved':
                return JsonResponse({'status': 'verified'})

        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostListDetailfilter(generics.ListAPIView):
    """
    Connect method docstring: Brief description of the connect method.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^title']


class Predict(APIView):
    """
    Connect method docstring: Brief description of the connect method.
    """

    def post(self, request):
        """
        Connect method docstring: Brief description of the connect method.
        """
        serializer = PredictionSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data['title']
            model = Model()
            prediction = model.compute_prediction(title)
            return Response(prediction, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# this is just to display all the replies of a certain comment
class RepliesList(generics.ListCreateAPIView):
    """
    Connect method docstring: Brief description of the connect method.
    """
    # # permission_classes = [IsAuthenticatedOrReadOnly]
    # # queryset = Comment.objects.filter()
    serializer_class = ReplySerializer

    def get_queryset(self):
        """
        Connect method docstring: Brief description of the connect method.
        """
        commentid = self.kwargs.get('id')
        print(commentid)
        replies = Comment.objects.filter(parent=commentid)
        print(replies)
        return replies

    def get_serializer_context(self):
        """
        Connect method docstring: Brief description of the connect method.
        """
        context = super().get_serializer_context()
        context['pk'] = self.kwargs.get('pk')
        context['id'] = self.kwargs.get('id')
        return context

    def post(self, request, *args, **kwargs):
        """
        Connect method docstring: Brief description of the connect method.
        """
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            # message = 'Comment Added'
            # user = request.user.email
            # send_notifications(request, user, message)

        return Response(serializer.data, status=status.HTTP_200_OK)


def get_notifications(request):
    notifications = Notifications.objects.all()
    serialized_notifications = [
        {'id': n.id, 'message': n.message} for n in notifications]
    return JsonResponse({'notifications': serialized_notifications})


class FileUploadView(generics.ListCreateAPIView):
    # parser_classes = [FileUploadParser]
    queryset = FileUploader.objects.all()
    serializer_class = FileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            file = serializer.validated_data['csv_file']

            file.open()
            file_content = file.read().decode('utf-8')
            file_buffer = io.StringIO(file_content)

            df = pd.read_csv(file_buffer)
            print(df.head())

            # if df.empty:
            #     return Response({'message': 'The uploaded file is empty or contains only headers.'}, status=status.HTTP_400_BAD_REQUEST)

            ecommerce_instances = []

            for index, row in df.iterrows():
                ecommerce_instance = Ecommerce(
                    product_name=row['product_name'],
                    product_description=row['product_description'],
                    iban=row['iban'],
                    quantity_in_stock=row['quantity_in_stock'],
                    product_price=row['product_price'],
                    product_category=row['product_category'],
                    product_brand=row['product_brand'],
                    product_weight=row['product_weight'],
                    product_color=row['product_color'],
                    product_rating=row['product_rating']
                )
                ecommerce_instances.append(ecommerce_instance)

            Ecommerce.objects.bulk_create(ecommerce_instances)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # return Response({'message': 'serializer is invalid!'}, serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPEmail(APIView):
    def post(self, request):
        try:
            serializer = VerifyAccountSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                email = serializer.validated_data['email']
                print(email)
                otp = serializer.validated_data['otp']

                user = User.objects.get(email=email)

                if not user:
                    return Response({'message': 'User doesnt exists!'}, status=status.HTTP_404_NOT_FOUND)

                if not user.otp == otp:
                    return Response({'message': 'Otp is not correct!'}, status=status.HTTP_404_NOT_FOUND)

                user.is_active = True
                user.save()
                print(user.is_active)

                return Response({'message': 'User active!'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # return Response({'message': 'User active!'}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CartCheckout(APIView):
#     def Post(self, request):
#         """
#         Connect method docstring: Brief description of the connect method.
#         """
#         serializer = CartCheckoutSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):

#             user = serializer.validated_data['user']
#             company_name = serializer.validated_data['company_name']
#             country = serializer.validated_data['country']
#             street_address = serializer.validated_data['street_address']
#             state = serializer.validated_data['state']
#             zip_code = serializer.validated_data['zip_code']
#             notes = serializer.validated_data['notes']

#             UserAddress.objects.create(user=user, company_name=company_name, country=country,
#                                        street_address=street_address, state=state, zip_code=zip_code, notes=notes)

#             return Response({'message': 'user address stored'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'message': 'User Not Authenticated'}, status=status.HTTP_200_OK)

class UserAddressCreateView(generics.CreateAPIView):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer


class CartCreateView(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartCheckoutSerializer


class Currency(APIView):
    def get(self, request):
        response = requests.get(
            "https://ipgeolocation.abstractapi.com/v1/?api_key=1c222f349c144c0cb2456f2d30661713&ip_address=116.58.60.117")
        print(response.status_code)
        print(response.content)

        if response.status_code == 200:
            response_json = response.json()

            currency_info = response_json["currency"]
            currency_name = currency_info["currency_name"]
            city = response_json["city"]

            return Response({
                'message': 'Location working!',
                'status_code': response.status_code,
                'content': response_json,
                "currency_name": currency_name,
                "city": city
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'Failed to get location information',
                'status_code': response.status_code
            }, status=response.status_code)
