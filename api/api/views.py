from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import URLSerializer


class ListApiUrls(APIView):
    permission_classes = []

    def get(self, request, format=None):
        from .urls import urlpatterns
        serializer = URLSerializer(context={'request': request})
        return Response(serializer.to_representation(urlpatterns))
