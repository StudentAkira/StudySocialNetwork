import json, random
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import CustomUser, Profile
from rest_framework.response import Response
import requests
from .serializers import CustomUserSerializer, ProfileSerializer

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
        profile = Profile.objects.filter(user=user).get()
        return Response({'username': user.username, 'avatar':str(profile.avatar)})


class GetUsers(APIView):
    def get(self, request, pk):
        users_db = list(CustomUser.objects.select_related('profile').all())
        paginator = Paginator(users_db, 20)
        pagenumber = pk
        if pagenumber > len(paginator.page_range):
            pagenumber = len(paginator.page_range)
        paginated_users = paginator.get_page(pagenumber)

        usersData = []
        for i in range(len(list(paginated_users))):
            user_serializer = CustomUserSerializer(paginated_users[i])
            profile_serializer = ProfileSerializer(paginated_users[i].profile)
            usersData += [[user_serializer.data, profile_serializer.data]]
        return Response({'UsersData': usersData, 'AmountOfUsers': len(users_db)})


class NewUserAPIView(APIView):
        def get(self, request):
            for i in range(250):
                data = {
                    'username':'user'+str(i),
                    'password':'user'+str(i)
                }
                new_user_serializer = CustomUserSerializer(data=data)
                new_user_serializer.is_valid()
                new_user = new_user_serializer.create(validated_data=new_user_serializer.validated_data)
            return Response({'username': new_user.username})
