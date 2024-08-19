"""
Connect method docstring: Brief description of the connect method.
"""

from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .models import Post, Comment, Category, Ecommerce, UserAddress, Cart, FileUploader

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Connect method docstring: Brief description of the connect method.
    """
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        """
        Connect method docstring: Brief description of the connect method.
        """
        model = User
        fields = ['email', 'username', 'password', 'is_creator', 'is_editor']

    def create(self, validated_data):
        """
        Connect method docstring: Brief description of the connect method.
        """
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Connect method docstring: Brief description of the connect method.
    """
    password = serializers.CharField(min_length=8, write_only=True)
    email = serializers.EmailField()

    class Meta:
        """
        Connect method docstring: Brief description of the connect method.
        """
        model = User
        fields = ['email', 'password']


class CommentSerializer(serializers.ModelSerializer):
    """
    Connect method docstring: Brief description of the connect method.
    """
    body = serializers.CharField(min_length=10)
    author = serializers.ReadOnlyField(source='user.username')

    class Meta:
        """
        Connect method docstring: Brief description of the connect method.
        """
        model = Comment
        fields = ['id', 'body', 'post', 'author', 'parent']


class CategorySerializer(serializers.ModelSerializer):
    """
    Connect method docstring: Brief description of the connect method.
    """
    name = serializers.CharField()

    class Meta:
        """
        Connect method docstring: Brief description of the connect method.
        """
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    """
    Connect method docstring: Brief description of the connect method.
    """
    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = serializers.CharField()
    image = serializers.ImageField()
    thumbnail = serializers.CharField(required=False)
    excerpt = serializers.CharField()
    content = serializers.CharField()
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    is_top = serializers.BooleanField()
    is_featured = serializers.BooleanField()
    is_trending = serializers.BooleanField(read_only=True)
    is_popular = serializers.BooleanField(read_only=True)
    # likes = serializers.IntegerField(read_only=True)
    views = serializers.IntegerField(read_only=True)
    is_post_pro = serializers.BooleanField()

    class Meta:
        """
        Connect method docstring: Brief description of the connect method.
        """
        model = Post
        fields = ['id', 'title', 'category',
                  'excerpt', 'content', 'author', 'image', 'thumbnail', 'is_top',
                  'is_featured', 'views', 'is_trending', 'is_popular',
                  'is_post_pro']


class PostDetailSerializer(serializers.ModelSerializer):
    """
    Connect method docstring: Brief description of the connect method.
    """

    title = serializers.CharField(max_length=250)
    image = serializers.ImageField(required=False)
    thumbnail = serializers.CharField(required=False)
    excerpt = serializers.CharField()
    content = serializers.CharField()
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, allow_empty=True, read_only=True)
    views = serializers.IntegerField(read_only=True)
    is_post_pro = serializers.BooleanField(read_only=True)
    # likes = serializers.IntegerField(read_only=True)
    is_trending = serializers.BooleanField()
    is_popular = serializers.BooleanField()

    class Meta:
        """
        Connect method docstring: Brief description of the connect method.
        """
        model = Post
        fields = ['id', 'title', 'category',
                  'excerpt', 'content', 'author',
                  'comments', 'views', 'image', 'thumbnail',
                  'is_post_pro', 'is_trending',
                  'is_popular']

    def update(self, instance, validated_data):
        """
        Connect method docstring: Brief description of the connect method.
        """

        instance.title = validated_data.get('title', instance.title)
        instance.excerpt = validated_data.get('excerpt', instance.excerpt)
        instance.content = validated_data.get('content', instance.content)
        instance.author = validated_data.get('author', instance.author)
        instance.category = validated_data.get('category', instance.category)
        instance.image = validated_data.get('image', instance.image)

        instance.save()
        return instance


class CommentDetailSerializer(serializers.ModelSerializer):
    """
    Connect method docstring: Brief description of the connect method.
    """
    post = serializers.PrimaryKeyRelatedField(queryset=Post.postobjects.all())
    # parent = serializers.PrimaryKeyRelatedField(
    #     queryset=Comment.objects.all(), required=False)

    class Meta:
        """
        Connect method docstring: Brief description of the connect method.
        """
        model = Comment
        fields = ['id', 'body', 'user', 'parent', 'post']

    def create(self, validated_data):
        """
        Connect method docstring: Brief description of the connect method.
        """
        post_pk = self.context.get('pk')
        post = Post.objects.get(pk=post_pk)
        validated_data['post'] = post
        return super().create(validated_data)


class Otpserializer(serializers.Serializer):
    """
    Connect method docstring: Brief description of the connect method.
    """
    otp = serializers.IntegerField(required=False)
    number = serializers.CharField()
    user_id = serializers.IntegerField(required=False)

    class Meta:
        """
        Connect method docstring: Brief description of the connect method.
        """
        fields = ['number', 'otp', 'user_id']


class PredictionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)


class ReplySerializer(serializers.Serializer):
    """
    Connect method docstring: Brief description of the connect method.
    """
    id = serializers.IntegerField(read_only=True)
    body = serializers.CharField(min_length=10)
    author = serializers.ReadOnlyField(source='user.username')
    post = PostDetailSerializer(read_only=True)

    class Meta:
        """
        Connect method docstring: Brief description of the connect method.
        """
        model = Comment
        fields = ['id', 'body', 'post', 'author', 'parent']


class FileSerializer(serializers.ModelSerializer):
    """
    Connect method docstring: Brief description of the connect method.
    """
    csv_file = serializers.FileField()

    class Meta:
        """
        Connect method docstring: Brief description of the connect method.
        """
        model = FileUploader
        fields = '__all__'


class EcommerceSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(max_length=100)
    iban = serializers.CharField(max_length=200)
    quantity_in_stock = serializers.IntegerField()
    product_price = serializers.FloatField()
    product_category = serializers.CharField(max_length=200)
    product_brand = serializers.CharField(max_length=200)
    product_rating = serializers.FloatField()

    class Meta:
        """
        Connect method docstring: Brief description of the connect method.
        """
        model = Ecommerce
        fields = ['product_name', 'iban', 'quantity_in_stock', 'product_price',
                  'product_category', 'product_brand', 'product_rating']


class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=4, required=True)


class CurrentUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = '__all__'


class CartCheckoutSerializer(serializers.ModelSerializer):

    # user = serializers.StringRelatedField(read_only=True)
    # company_name = serializers.CharField()
    # country = serializers.ChoiceField(choices, allow_blank=False)
    # street_address = serializers.CharField()
    # city = serializers.CharField()
    # state = serializers.CharField()
    # zip_code = serializers.IntegerField()
    # notes = serializers.CharField()

    order_price = serializers.FloatField()

    class Meta:
        """
        Connect method docstring: Brief description of the connect method.
        """
        model = Cart
        fields = '__all__'
