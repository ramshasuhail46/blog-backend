"""
Connect method docstring: Brief description of the connect method.
"""

import graphene
from graphene_django import DjangoObjectType

from .models import Post


class PostType(DjangoObjectType):
    """
    Connect method docstring: Brief description of the connect method.
    """
    class Meta:
        """
        Connect method docstring: Brief description of the connect method.
        """
        model = Post
        fields = ("id", "category", "title", "excerpt",
                  "likes", "views", "is_popular")


class Query(graphene.ObjectType):
    """
    Connect method docstring: Brief description of the connect method.
    """

    all_post = graphene.List(PostType)

    def resolve_all_post(self, root):
        """
        Connect method docstring: Brief description of the connect method.
        """
        return Post.objects.all()


schema = graphene.Schema(query=Query)
