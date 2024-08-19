"""
Connect method docstring: Brief description of the connect method.
"""
from rest_framework import serializers

from .models import ContactForm, NewsLetterUsers


class ContactFormSerializer(serializers.ModelSerializer):
    """
    Connect method docstring: Brief description of the connect method.
    """
    email = serializers.EmailField()
    subject = serializers.CharField()
    message = serializers.CharField(max_length=200)
    name = serializers.CharField()

    class Meta:
        """
        Connect method docstring: Brief description of the connect method.
        """
        model = ContactForm
        fields = ['email', 'subject', 'message', 'name']


class NewsLetterUsersSerializer(serializers.ModelSerializer):
    """
    Connect method docstring: Brief description of the connect method.
    """
    email = serializers.EmailField()

    class Meta:
        """
        Connect method docstring: Brief description of the connect method.
        """
        model = NewsLetterUsers
        fields = ['email']
