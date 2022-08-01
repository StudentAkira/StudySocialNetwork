from rest_framework import serializers
from .models import CustomUser, Profile, Post


class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=4)

    class Meta:
        model = CustomUser
        fields = ['id','username']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(default=0)
    status = serializers.CharField(default='', max_length=127, allow_blank=True, allow_null=True)
    description = serializers.CharField(default='', max_length=511, allow_blank=True, allow_null=True)

    class Meta:
        model = Profile
        fields = ['rating', 'status', 'description', 'avatar']

    def create(self, validated_data):
        return Profile.objects.create(user_id=self.user_id,)


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    article = serializers.CharField(default='', max_length=255)
    text = serializers.CharField(default='', max_length=4095)
    likes = serializers.IntegerField(default=0)

    class Meta:
        model = CustomUser
        fields = ['id','owner','article','text','likes']

    def create(self, validated_data):
        return Post.objects.create(**validated_data)


class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    position = serializers.IntegerField(default=0)
    post = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['image','position','post']
