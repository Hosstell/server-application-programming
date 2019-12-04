import graphene
from .types import PictureType
from ..models import Picture


class Query(graphene.ObjectType):
    get_all_my_pictures = graphene.List(PictureType)
    get_picture = graphene.Field(PictureType, picture_id=graphene.String())

    def resolve_get_all_my_pictures(self, info):
        user = info.context.user
        return Picture.objects.filter(user_id=user.id).order_by('-load_date')

    def resolve_get_picture(self, info, picture_id=None):
        if not picture_id:
            return []
        return Picture.objects.get(id=picture_id)
