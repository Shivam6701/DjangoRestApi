from distutils.command.install import SCHEME_KEYS
import email
import imp
import bcrypt
from django.shortcuts import render
from django.contrib.auth.hashers import make_password,check_password
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from passlib.hash import bcrypt
from tutorials.models import Post,User
from tutorials.serializers import PostSerializer,UserSerializer,UserOutSerializer,UserLogin
from rest_framework.decorators import api_view

@api_view(['GET', 'POST', 'DELETE'])
def post_list(request):
    if request.method == 'GET':
        post = Post.objects.all()
        
        title = request.GET.get('title', None)
        if title is not None:
            post = post.filter(title__icontains=title)

        posts_serializer = PostSerializer(post, many=True)
        return JsonResponse(posts_serializer.data, safe=False)
        # 'safe=False' for objects serialization
       
    elif request.method == 'POST':
        post_data = JSONParser().parse(request)
        post_serializer = PostSerializer(data=post_data)
        if post_serializer.is_valid():
            post_serializer.save()
            return JsonResponse(post_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Post.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        post_serializer = PostSerializer(post)
        return JsonResponse(post_serializer.data)

    elif request.method == 'PUT':
        post_data = JSONParser().parse(request)
        post_serializer = PostSerializer(post, data=post_data)
        if post_serializer.is_valid():
            post_serializer.save()
            return JsonResponse(post_serializer.data)
        return JsonResponse(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def post_list_published(request):
    tutorials = Post.objects.filter(published=True)

    if request.method == 'GET':
        post_serializer = PostSerializer(tutorials, many=True)
        return JsonResponse(post_serializer.data, safe=False)


@api_view(['POST'])
def create_user(request):
    user_data = JSONParser().parse(request)
    user_data['password']=bcrypt.hash(user_data['password'])
    user_serializer = UserSerializer(data=user_data)
    if user_serializer.is_valid():
        user_serializer.save()
        return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        userOut_serializer = UserOutSerializer(user)
        return JsonResponse(userOut_serializer.data)

    elif request.method == 'PUT':
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({'message': 'User was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
def user_Login(request):
    
    user_data = JSONParser().parse(request)
    password = user_data['password']
    email = user_data['email']
        
    try:
        user = User.objects.get(email=email)
        if not bcrypt.verify (password,user.password) :
            return JsonResponse({'message': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)
        else:
            #create token
            return JsonResponse({"token":"exampleToken"})
    except User.DoesNotExist:
        return JsonResponse({'message': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)
