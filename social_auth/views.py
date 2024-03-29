# django imports
from django.shortcuts import render

# rest_framework imports
from rest_framework import generics, status
from rest_framework.response import Response

# app imports
from .serializers import GoogleLoginSerializer

# Create your views here.


class GoogleLoginView(generics.GenericAPIView):
    serializer_class = GoogleLoginSerializer
    http_method_names = ["post"]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data["auth_token"]
        return Response(data, status=status.HTTP_200_OK)
