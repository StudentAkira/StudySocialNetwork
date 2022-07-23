from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class TestView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return render(request,
                      template_name='test.html',
                      context={'username': request.user.username})
