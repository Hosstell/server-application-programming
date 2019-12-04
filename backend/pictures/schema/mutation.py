import graphene
from graphene_file_upload.scalars import Upload
from ..models import Picture
from .network.recognize import get_numbers
from django.core.files import File
from .types import PictureText
import time


class RecognizeImage(graphene.Mutation):
    image_id = graphene.String()
    image_text = graphene.String()

    class Arguments:
        file = Upload(required=True)

    def mutate(self, info, file, **kwargs):
        user = info.context.user
        numbers, numbers_line  = get_numbers(file.file)
        numbers_line = list(map(lambda x: str(x), numbers_line))
        numbers_line = ''.join(numbers_line)

        picture = Picture.objects.create(user_id=user.id, file=file, text=numbers_line)
        for index, number in enumerate(numbers):
            filename = 'my_file.png'
            number['image'].save(filename)
            file = open(filename, 'rb')
            Picture.objects.create(parent_picture=picture, file=File(file), text=number['number'])
            file.close()

        return RecognizeImage(image_id=picture.id, image_text=numbers_line)


class ChangePictureText(graphene.Mutation):
    result = graphene.Boolean()

    class Arguments:
        new_text = graphene.List(PictureText)

    def mutate(self, info, new_text):
        for new_data in new_text:
            Picture.objects.filter(id=new_data.picture_id).update(text=new_data.new_text)

        return ChangePictureText(result=True)

class Mutation(graphene.ObjectType):
    recognize_image = RecognizeImage.Field()
    new_text = ChangePictureText.Field()
