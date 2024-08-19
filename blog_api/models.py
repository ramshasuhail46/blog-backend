"""
Connect method docstring: Brief description of the connect method.
"""
import uuid
from PIL import Image
from io import BytesIO

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.db.models import UniqueConstraint
from django.core.files.uploadedfile import InMemoryUploadedFile

import sys

# Create your models here.

User = get_user_model()


class Category(models.Model):
    """
    Connect method docstring: Brief description of the connect method.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Connect method docstring: Brief description of the connect method.
        """
        return f"Name: {self.name}"


def upload_to(instance, filename):
    """
    Connect method docstring: Brief description of the connect method.
    """
    return f'posts/{filename}'.format(filename=filename)


# def upload_thumbnail_to(instance, filename):
#     """
#     Connect method docstring: Brief description of the connect method.
#     """
#     return f'thumbnail/{filename}'.format(filename=filename)


class Post(models.Model):
    """
    Connect method docstring: Brief description of the connect method.
    """

    class PostObjects(models.Manager):
        """
        Connect method docstring: Brief description of the connect method.
        """

        def get_queryset(self):
            """
            Connect method docstring: Brief description of the connect method.
            """
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT)
    title = models.CharField(max_length=250)
    image = models.ImageField(
        "Image", upload_to=upload_to, default='posts/default.jpg')
    thumbnail = models.ImageField(
        "Thumbnail", upload_to=upload_to, default='posts/default.jpg')
    excerpt = models.TextField(null=True)
    content = models.TextField()
    slug = models.SlugField(
        max_length=250, unique_for_date='published')
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    status = models.CharField(
        max_length=10, choices=options, default='published')
    is_top = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    # likes = models.ForeignKey(
    #     Like, on_delete=models.CASCADE, related_name='blog_posts')
    views = models.IntegerField(default=0)
    to_be_posted = models.DateTimeField(default=timezone.now, null=True, blank=True
                                        )
    is_post_pro = models.BooleanField(default=False)

    objects = models.Manager()  # default manager
    postobjects = PostObjects()  # custom manager

    class Meta:

        """
        Connect method docstring: Brief description of the connect method.
        """
        ordering = ('-published', 'is_top', 'is_featured')

    def __str__(self):
        """
        Connect method docstring: Brief description of the connect method.
        """
        return f"Title: {self.title}"


class Like(models.Model):
    """
    Connect method docstring: Brief description of the connect method.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, related_name='likes')
    action = models.CharField(max_length=200, default='like')
    # objects = models.Manager()


class Comment(models.Model):
    """
    Connect method docstring: Brief description of the connect method.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, related_name='comments')
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        Connect method docstring: Brief description of the connect method.
        """
        return f"Body: {self.body}"


class Notifications(models.Model):
    """
    Connect method docstring: Brief description of the connect method.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, related_name='notification')
    read_status = models.BooleanField(default=False)
    to = models.ForeignKey(User, on_delete=models.CASCADE,
                           related_name='notif_to', null=True)

    def __str__(self):
        """
        Connect method docstring: Brief description of the connect method.
        """
        return f"Message: {self.message}"


class Ecommerce(models.Model):
    """
    Connect method docstring: Brief description of the connect method.
    """
    product_name = models.CharField(max_length=100, default='red')
    product_description = models.CharField(max_length=100, default='red')
    iban = models.CharField(max_length=200, default='red')
    quantity_in_stock = models.IntegerField(default=1)
    product_price = models.FloatField(default=1.0)
    product_category = models.CharField(max_length=200, default='red')
    product_brand = models.CharField(max_length=200, default='red')
    product_weight = models.FloatField(default=1.0)
    product_color = models.CharField(max_length=100, default='red')
    product_rating = models.IntegerField(default=1)


class FileUploader(models.Model):
    csv_file = models.FileField(upload_to="csv")

    def __str__(self):
        """
        Connect method docstring: Brief description of the connect method.
        """
        return f"{self.csv_file}"


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Connect method docstring: Brief description of the connect method.
        """
        return f"{self.name}"


class ProductTags(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        """
        Connect method docstring: Brief description of the connect method.
        """
        return f"{self.tag}"


class Sizes(models.Model):

    options = (
        ('x', 'X'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
    )

    name = models.CharField(
        max_length=20, choices=options, default=None)
    stock = models.IntegerField(default=0)

    def __str__(self):
        """
        Connect method docstring: Brief description of the connect method.
        """
        return f"{self.name}"


class Colours(models.Model):
    options = (
        ('black', 'Black'),
        ('blue', 'Blue'),
        ('white', 'White'),
        ('brown', 'Brown'),
    )

    colour = models.CharField(
        max_length=20, default="Black")

    def __str__(self):
        """
        Connect method docstring: Brief description of the connect method.
        """
        return f"{self.colour}"


class Variation(models.Model):
    colour = models.ForeignKey(Colours, on_delete=models.CASCADE)
    image = models.ImageField()
    size = models.ManyToManyField(Sizes)

    def __str__(self):
        return f"{self.colour}"


class Products(models.Model):

    sku = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField()
    offerEnd = models.DateField(default=timezone.now)
    new = models.BooleanField(default=False)
    rating = models.PositiveIntegerField()
    saleCount = models.PositiveIntegerField()
    category = models.ManyToManyField(ProductCategory)
    tag = models.ManyToManyField(ProductTags)
    shortdescription = models.TextField(max_length=300)
    longdescription = models.TextField(max_length=1000)
    image = models.ImageField()
    variations = models.ManyToManyField(Variation)

    def __str__(self):
        return f"{self.name}"


class UserAddress(models.Model):

    options = (
        ('azerbaijan', 'Azerbaijan'),
        ('bahamas', 'Bahamas'),
        ('bahrain', 'Bahrain'),
        ('bangladesh', 'Bangladesh'),
        ('barbados', 'Barbados'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    country = models.CharField(
        max_length=20, choices=options, default=None)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip_code = models.IntegerField()
    notes = models.TextField(null=True)

    def __str__(self):
        return f"{self.company_name}"


class Cart(models.Model):
    order_price = models.FloatField(default=0.0)
    products_chosen = models.ManyToManyField(Products)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.order_price}"
