"""
Connect method docstring: Brief description of the connect method.
"""

from django.contrib import admin

from users.models import User
from contact.models import ContactForm, NewsLetterUsers

from .models import Post, Category, Comment, Notifications, Like, Ecommerce, FileUploader, UserAddress, ProductCategory, ProductTags, Sizes, Colours, Variation, Products, Cart

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Connect method docstring: Brief description of the connect method.
    """
    list_display = ('title', 'id', 'status', 'slug',
                    'author', 'is_top', 'is_featured',
                    'is_trending', 'to_be_posted', 'is_post_pro')
    prepopulated_fields = {'slug': ('title',), }


class CommentAdmin(admin.ModelAdmin):
    """
    Connect method docstring: Brief description of the connect method.
    """
    list_display = ('id', 'body', 'post')


class CategoryAdmin(admin.ModelAdmin):
    """
    Connect method docstring: Brief description of the connect method.
    """
    list_display = ('name', 'id')


class UserAdmin(admin.ModelAdmin):
    """
    Connect method docstring: Brief description of the connect method.
    """
    list_display = ('email', 'is_pro',)


class NotificationsAdmin(admin.ModelAdmin):
    """
    Connect method docstring: Brief description of the connect method.
    """
    list_display = ('user', 'message', 'post', 'read_status', 'to',)


class LikeAdmin(admin.ModelAdmin):
    """
    Connect method docstring: Brief description of the connect method.
    """
    list_display = ('id', 'user', 'post',)


class EcommerceAdmin(admin.ModelAdmin):
    """
    Connect method docstring: Brief description of the connect method.
    """
    list_display = ('product_name', 'iban', 'quantity_in_stock', 'product_price',
                    'product_category', 'product_brand', 'product_rating',)


class UserAddressAdmin(admin.ModelAdmin):
    """
    Connect method docstring: Brief description of the connect method.
    """
    list_display = ('user', 'city', 'country', 'zip_code',
                    'notes',)


class VariationAdmin(admin.ModelAdmin):
    """
    Connect method docstring: Brief description of the connect method.
    """
    list_display = ('colour',)


admin.site.register(ProductCategory)

admin.site.register(ProductTags)

admin.site.register(Sizes)

admin.site.register(Colours)

admin.site.register(Variation, VariationAdmin)

admin.site.register(Products)

admin.site.register(ContactForm)

admin.site.register(UserAddress, UserAddressAdmin)

admin.site.register(FileUploader)

admin.site.register(Ecommerce, EcommerceAdmin)

admin.site.register(Like, LikeAdmin)

admin.site.register(Notifications, NotificationsAdmin)

admin.site.register(NewsLetterUsers)

admin.site.register(User, UserAdmin)

admin.site.register(Comment, CommentAdmin)

admin.site.register(Category, CategoryAdmin)

admin.site.register(Cart)
