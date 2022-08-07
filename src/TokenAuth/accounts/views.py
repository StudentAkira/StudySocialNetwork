import json, random, os
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import CustomUser, Profile, PostImage, Post
from rest_framework.response import Response
import requests
from .serializers import CustomUserSerializer, ProfileSerializer, PostSerializer, PostImageSerializer
from TokenAuth.settings import BASE_DIR, MEDIA_ROOT

class TokenLoginAPIView(APIView):
    def get(self, request):
        user = request.user
        username = request.user.username
        password = ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(20)])
        user.set_password(password)
        user.save()
        data = {
            'username': username,
            'password': password,
        }
        url = 'http://127.0.0.1:8000/auth/token/login'
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        token = json.loads(response.text)['auth_token']
        return redirect('http://127.0.0.1:3001/?token='+token)


class CheckAuthAPIView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'userId': -1})
        userId = request.user.id
        return Response({'userId': userId})


class ChangeAvatarAPIView(APIView):
    def post(self, request):
        print(request.data)
        print(request.data['avatar'])
        profile = request.user.profile
        profile.avatar.delete()
        profile.avatar = request.data['avatar']
        profile.save()
        return Response({'username': 'pass'})


class NewUserAPIView(APIView):
        def post(self, request):
            data = {
                'username':request.data['data']['username'],
                'password':request.data['data']['password']
            }
            new_user_serializer = CustomUserSerializer(data=data)
            new_user_serializer.is_valid()
            new_user = new_user_serializer.create(validated_data=new_user_serializer.validated_data)
            return Response({'username': 'nothing'})


class CreateNewPostAPIView(APIView):
    def post(self, request):
        #TODO
        if not request.user.is_authenticated:
            return Response({'error':'unauthorizer'})

        data = request.data.dict()
        print(data)
        amount_of_images = len(data['ImageLocations'].split(','))-1
        locations_of_images = data['ImageLocations'].split(',')
        if amount_of_images > 4:
            return Response({'error':'a lot of img'})

        try:
            new_post_serializer = PostSerializer(data=data)
            new_post_serializer.is_valid()
            print(new_post_serializer.validated_data, ' ', new_post_serializer.errors)
            post = new_post_serializer.create(validated_data=new_post_serializer.validated_data)
            post.owner = request.user
            post.save()

            for image_index in range(amount_of_images):
                PostImage.objects.create(
                    image=data[f'image{image_index}'],
                    position=locations_of_images[image_index],
                    post=post,
                )
            return Response({'status':'success', 'redirect_to':'/posts/post/'+str(post.id)+'/'})
        except:
            return Response({'status':'error','message':'oops something went wrong'})


class EditPostAPIView(APIView):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'User':'unauthorizer'})
        try:
            post = Post.objects.prefetch_related('postimage_set').get(id=pk)
        except:
            return Response({'message':'no such post'})
        if post.owner.id != request.user.id:
            return Response({'error': 'u are not owner'})
        try:
            data = dict(request.data)

            post.text = data['text'][0]
            post.article = data['article'][0]
            post.save()

            ordered_postimage_instanses = list(post._prefetched_objects_cache['postimage_set'].order_by('position'))
            new_image_positions = data['image_postitions'][0].split(',')
            image_order_numbers = data['images_order_numbers'][0].split(',')


            for post_image_instanse in ordered_postimage_instanses:
                post_image_instanse.position = new_image_positions[ordered_postimage_instanses.index(post_image_instanse)]
                post_image_instanse.save()

            images_changed = True if image_order_numbers != [''] else False

            if images_changed:
                for image_order_number in image_order_numbers:
                    os.remove(MEDIA_ROOT+'/'+str(ordered_postimage_instanses[int(image_order_number)].image))
                    ordered_postimage_instanses[int(image_order_number)].image = data[image_order_number][0]
                    ordered_postimage_instanses[int(image_order_number)].save()

            return Response({'status':'success', 'redirect_to':'/posts/post/'+str(post.id)+'/'})
        except:
            return Response({'status':'error','message':'oops something went wrong'})



class GetPostAPIView(APIView):
    def get(self, request, pk):
        images = []
        try:
            post = Post.objects.prefetch_related('postimage_set').get(id=pk)
        except:
            return Response({'message':'no such post'})
        for image_index in range(len(post._prefetched_objects_cache['postimage_set'])):
            images += [[
                        str(post._prefetched_objects_cache['postimage_set'][image_index].image),
                        str(post._prefetched_objects_cache['postimage_set'][image_index].position)
                      ]]

        OwnerData = ''

        try :
            owner = CustomUser.objects.select_related('profile').get(id=post.owner.id)
            OwnerData = {
                    'exists': True,
                    'id': owner.id,
                    'username':owner.username,
                    'avatar':str(owner.profile.avatar),
                    'rating':owner.profile.rating,
            }

        except:
            OwnerData = {
                    'exists': False,
                    'id':owner.id,
                    'username':'',
                    'avatar':'',
                    'rating':'',
            }
        post_serializer = PostSerializer(post)
        isliked = request.user.liked.filter(id=pk).exists() if request.user.is_authenticated else False
        print(isliked, ' ', request.user.is_authenticated)
        return Response({'OwnerData':OwnerData,
                        'PostData': post_serializer.data,
                        'images': images,
                        'isliked': isliked,
                        })


class GetPostsAPIView(APIView):
    def get(self, request, pk):
        posts_db = list(Post.objects.prefetch_related('postimage_set').all())
        paginator = Paginator(posts_db, 20)
        pagenumber = pk
        if pagenumber > len(paginator.page_range):
            pagenumber = len(paginator.page_range)
        paginated_posts = paginator.get_page(pagenumber)

        posts = []
        for post_index in range(len(list(paginated_posts))):
            post_serializer = PostSerializer(paginated_posts[post_index])
            posts += [[post_serializer.data, []]]
            for image in paginated_posts[post_index]._prefetched_objects_cache['postimage_set']:
                new_post_image_serializer = PostImageSerializer(image)
                posts[post_index][1] += [new_post_image_serializer.data]

        return Response({'PostsData':posts,'AmountOfPosts': len(posts_db)})


class GetUserAPIView(APIView):
    def get(self, request, pk):
        user = CustomUser.objects.get(id=pk)
        profile = Profile.objects.filter(user=user).get()
        print(profile.avatar)
        return Response({'username': user.username, 'avatar':str(profile.avatar), 'id':user.id})


class GetUsersAPIView(APIView):
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


class DeletePostAPIView(APIView):
    def get(self, request, pk):
        post = Post.objects.prefetch_related('postimage_set').get(id=pk)
        if not request.user.is_authenticated:
            return Response({'error': 'unauthorized'})
        if post.owner.id != request.user.id:
            return Response({'error':'this is not yours post'})

        try:
            for image in post._prefetched_objects_cache['postimage_set']:
                os.remove(MEDIA_ROOT+'/'+str(image.image))
                image.delete()
            post.delete()
            return Response({'status':'success', 'redirect_to':'http://127.0.0.1:3001/me'})
        except:
            return Response({'status':'error', 'message':'somesing went wrong'})


class LikeAPIView(APIView):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'status':'error', 'message':'unauthorized'})
        user = request.user
        post_to_like = Post.objects.get(id=pk)
        like = user.liked.filter(id=pk)
        if like.exists():
            user.liked.remove(post_to_like)
            post_to_like.remove_like()
            post_to_like.save()
            user.save()
            return Response({'status':'success', 'message':'like removed'})

        user.liked.add(post_to_like)
        post_to_like.add_like()
        post_to_like.save()
        user.save()
        return Response({'status':'success', 'message':'like added'})


class Test(APIView):
    def get(self, request):
        return Response({'test': 'test'})
