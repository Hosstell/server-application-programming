from graphene_django import DjangoObjectType
from ..models import Picture
import graphene


class PictureType(DjangoObjectType):
    class Meta:
        model = Picture


class PictureText(graphene.InputObjectType):
    picture_id = graphene.String()
    new_text = graphene.String()