import json
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import CustomUser, Profile
from rest_framework.response import Response
import requests
from .serializers import CustomUserSerializer

class TokenLogin(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            params = dict(request.query_params)
            username = params['username'][0]
            password = params['password'][0]
            data = {
                'username': username,
                'password': password,
            }
            url = 'http://127.0.0.1:8000/auth/token/login'
            headers = {'Content-type': 'application/json'}
            response = requests.post(url, data=json.dumps(data), headers=headers)
            token = json.loads(response.text)['auth_token']
            return redirect('http://127.0.0.1:3001/Page1?token='+token)

        user = request.user
        username = request.user.username
        password = ''.join([chr(i) for i in range(100, 120)])
        user.set_password(password)
        data = {
            'username': username,
            'password': password,
        }
        url = 'http://127.0.0.1:8000/auth/token/login'
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        token = json.loads(response.text)['auth_token']
        return redirect('http://127.0.0.1:3001/Page1?token='+token)


class CheckAuth(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'userId': -1})
        userId = request.user.id
        return Response({'userId': userId})


class GetUserAPIView(APIView):
    def get(self, request, pk):
        user = CustomUser.objects.get(id=pk)
        return Response({'username': user.username})
