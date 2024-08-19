"""
Connect method docstring: Brief description of the connect method.
"""
from django.db import models

# Create your models here.


class ContactForm(models.Model):
    """
    Connect method docstring: Brief description of the connect method.
    """
    email = models.EmailField()
    name = models.CharField(max_length=100, default='name')
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        """
        Connect method docstring: Brief description of the connect method.
        """
        return f"Email: {self.email}"


class NewsLetterUsers(models.Model):
    """
    Connect method docstring: Brief description of the connect method.
    """
    email = models.EmailField(unique=True)

    def __str__(self):
        """
        Connect method docstring: Brief description of the connect method.
        """
        return f"Email: {self.email}"
