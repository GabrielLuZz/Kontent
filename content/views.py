from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.request import Request
from django.forms.models import model_to_dict

from .models import Content

from .validators import ContentValidator
# Create your views here.


class ContentView(APIView):
    def get(self, request):
        contents = Content.objects.all()

        contents_dict = [model_to_dict(Content) for Content in contents]

        return Response(contents_dict)

    def post(self, request):
        validator = ContentValidator(**request.data)

        if not validator.is_valid():
            return Response(validator.errors, status.HTTP_400_BAD_REQUEST)

        content = Content.objects.create(**request.data)
        content_dict = model_to_dict(content)

        return Response(content_dict, status.HTTP_201_CREATED)


class ContentDetailView(APIView):
    def get(self, request: Request, content_id: int) -> Response:
        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({
                "message": "Content not found"
            }, status.HTTP_404_NOT_FOUND)

        content_dict = model_to_dict(content)

        return Response(content_dict)

    def patch(self, request: Request, content_id: int) -> Response:
        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({
                "message": "Content not found"
            }, status.HTTP_404_NOT_FOUND)

        for key, value in request.data.items():
            # ipdb.set_trace()
            setattr(content, key, value)

        content.save()
        content_dict = model_to_dict(content)

        return Response(content_dict)

    def delete(self, request: Request, content_id: int) -> Response:
        # return Response({"data": "hello delete"})
        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({
                "message": "Content not found"
            }, status.HTTP_404_NOT_FOUND)

        content.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ContentFilterView(APIView):
    def get(self, request: Request) -> Response:
        title = request.query_params.get('title', None)

        contents = Content.objects.filter(title__icontains=title)

        contents_dict = [model_to_dict(content) for content in contents]

        return Response(contents_dict)
