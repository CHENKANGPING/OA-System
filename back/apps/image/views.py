import os

from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from shortuuid import uuid

from .serializers import UploadImageSerializer


class UploadImageAPIView(APIView):
    def post(self, request):
        serialize = UploadImageSerializer(data=request.data)
        if serialize.is_valid():
            file = serialize.validated_data.get('image')
            filename = uuid() + os.path.splitext(file.name)[-1]
            path = settings.MEDIA_ROOT / filename
            try:
                with open(path, 'wb') as fp:
                    for chunk in file.chunks():
                        fp.write(chunk)
            except Exception:
                return  Response({
                    "erron":1,
                    "message":"图片保存失败"
                })
            file_url = settings.MEDIA_URL + filename
            return Response({
                "erron" : 0,
                "data": {
                    "url":file_url,
                    "alt":"",
                    "href":file_url
                }
            })

        else:
            print(serialize.errors)
            return Response({
                "erron":1,
                "message":list(serialize.errors.values())[0][0]

            })
