"""
Connect method docstring: Brief description of the connect method.
"""

from django.urls import path

from contact.views import ContactFormView, NewsLetterUsersAPI
from .views import (
    UserLoginAPI,
    SendOtp,
    VerifyOtp,
    UserRegistrationAPI,
    PostList,
    PostDetail,
    CommentDetail,
    LikeView,
    CurrentUser,
    CategoryList,
    PostListDetailfilter,
    View,
    Predict,
    RepliesList,
    CommentList,
    get_notifications,
    FileUploadView,
    VerifyOTPEmail,
    CartCreateView,
    UserAddressCreateView,
    Currency
)


urlpatterns = [
    path('register/', UserRegistrationAPI.as_view(), name='register'),
    path('login/', UserLoginAPI.as_view(), name='login'),
    path('', PostList.as_view(), name="posts-list"),
    path('<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('<int:pk>/comments/', CommentDetail.as_view()),
    path('<int:pk>/commentlist/', CommentList.as_view()),
    path('contact/', ContactFormView.as_view(), name='contact-form'),
    path('newsletter/', NewsLetterUsersAPI.as_view(), name='contact-form'),
    path('<int:pk>/like/', LikeView.as_view(), name='like-post'),
    path('currentuser/', CurrentUser.as_view(), name='current-user'),
    path('category/', CategoryList.as_view(), name='category'),
    path('search/custom/', PostListDetailfilter.as_view(), name='filter'),
    path('sendotp/', SendOtp.as_view(), name='phone-verify'),
    # path('verifyotp/', VerifyOtp.as_view(), name='phone-verify'),
    path('<int:pk>/view/', View.as_view(), name='view-post'),
    path('predict/', Predict.as_view(), name='predict'),
    path('<int:pk>/comments/<int:id>/replies/', RepliesList.as_view()),
    path('notifications/', get_notifications, name="notifs"),
    path('upload/', FileUploadView.as_view(), name="upload"),
    path('verifyotp/', VerifyOTPEmail.as_view(), name='phone-verify'),
    path('cart/', CartCreateView.as_view(), name='cart'),
    path('address/', UserAddressCreateView.as_view(), name='address'),
    path('location/', Currency.as_view(), name='currency'),

]
