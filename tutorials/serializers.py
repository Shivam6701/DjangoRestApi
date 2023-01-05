from statistics import mode
from rest_framework import serializers
from tutorials.models import Post,User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id',
                  'title',
                  'content',
                  'published',
                  'owner_id',
                  )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'name',
                  'password',
                  'email',
                  )

class UserOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'name',
                  'email',
                  )

class UserLogin(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ('email',
                  'password',
                  )