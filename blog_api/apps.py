"""
Connect method docstring: Brief description of the connect method.
"""

from django.apps import AppConfig


class BlogApiConfig(AppConfig):
    """
    Connect method docstring: Brief description of the connect method.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog_api'

    # def ready(self):
    #     import blog_api.signals
