from django.db.models import fields
from rest_framework import serializers
from .models import Users
from .models import Categories
from .models import Post
from .models import Body

class UserSerializer(serializers.ModelSerializer):
	# PrimaryKeyRelatedField
	# author = serializers.PrimaryKeyRelatedField(read_only=True)
	class Meta:
		model = Users
		fields = ('userId', 'userName', 'passWord', 'avatar')

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Categories
		fields = ('categoryId', 'categoryName')

class PostsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('postId', 'name', 'description', 'createAt', 'mainImg', 'categoryId', 'userId')

class BodySerializer(serializers.ModelSerializer):
	# PrimaryKeyRelatedField
	# postId = serializers.PrimaryKeyRelatedField(many = False , read_only=True)
	class Meta:
		model = Body
		fields = ('bodyId', 'content', 'imageBody', 'tittleBody', 'postId')