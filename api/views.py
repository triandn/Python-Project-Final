from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Users , Categories , Post , Body
from .serializers import UserSerializer , CategorySerializer , PostsSerializer , BodySerializer
from rest_framework import status
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json
import string , random

token = "6793YUIO"

@csrf_exempt
def category_list(request):
	if request.method == 'GET':
		category = Categories.objects.all()
		category_serializer = CategorySerializer(category, many=True)
		return JsonResponse(category_serializer.data, safe=False)
	
	elif request.method == 'POST':
		category_data = JSONParser().parse(request)
		category_serializer = CategorySerializer(data=category_data)
		if category_serializer.is_valid():
			category_serializer.save()
			return JsonResponse(category_serializer.data, status=201)
		return JsonResponse(category_serializer.errors, status=400)

@csrf_exempt
def category_detail(request, categoryId):
	try:
		category = Categories.objects.get(categoryId=str(categoryId))
	except category.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		category_serializer = CategorySerializer(category)
		
		return JsonResponse(category_serializer.data)

	elif request.method == 'PUT':
		category_data = JSONParser().parse(request)
		category_serializer = CategorySerializer(category, data=category_data)
		if category_serializer.is_valid():
			category_serializer.save()
			return JsonResponse(category_serializer.data)
		return JsonResponse(category_serializer.errors, status=400)

	elif request.method == 'DELETE':
		category.delete()
		return HttpResponse(status=204)

@csrf_exempt
def user_list(request):
	
	if request.method == 'GET':
		user = Users.objects.all()
		user_arr = []
		user_serializer = UserSerializer(user, many=True)
		return JsonResponse(user_serializer.data, safe=False)
	
	elif request.method == 'POST':
		user_data = JSONParser().parse(request)
		user_serializer = UserSerializer(data=user_data)
		
		if user_serializer.is_valid():
			user_serializer.save()
			return JsonResponse(user_serializer.data, status=201)
		return JsonResponse(user_serializer.errors, status=400)

@csrf_exempt
def user_detail(request, userId):
	token_get = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
	print(token_get)
	if token_get.strip() == token:
		try:
			user = Users.objects.get(userId=str(userId))
		except user.DoesNotExist:
			return HttpResponse(status=404)

		if request.method == 'GET':
			user_serializer = UserSerializer(user)
			return JsonResponse(user_serializer.data)

		elif request.method == 'PUT':
			user_data = JSONParser().parse(request)
			user_serializer = UserSerializer(user, data=user_data)
			if user_serializer.is_valid():
				user_serializer.save()
				return JsonResponse(user_serializer.data)
			return JsonResponse(user_serializer.errors, status=400)

		elif request.method == 'DELETE':
			user.delete()
			return HttpResponse(status=204)

@csrf_exempt
def body_list(request):
	if request.method == 'GET':
		body = Body.objects.all()
		body_serializer = BodySerializer(body, many=True)
		return JsonResponse(body_serializer.data, safe=False)
	
	elif request.method == 'POST':
		body_data = JSONParser().parse(request)

		body_serializer = BodySerializer(data=body_data)
		print(body_serializer)
		if body_serializer.is_valid():
			body_serializer.save()
			return JsonResponse(body_serializer.data, status=201)
		return JsonResponse(body_serializer.errors, status=400)
@csrf_exempt
def body_detail(request, bodyId):
	body = Body.objects.get(bodyId=str(bodyId))
	if request.method == 'GET':
		body_serializer = BodySerializer(body)
		return JsonResponse(body_serializer.data)

	elif request.method == 'PUT':
		body_data = JSONParser().parse(request)
		body_serializer = BodySerializer(body, data=body_data)
		if body_serializer.is_valid():
			body_serializer.save()
			return JsonResponse(body_serializer.data)
		return JsonResponse(body_serializer.errors, status=400)

	elif request.method == 'DELETE':
		body_delete = Body.objects.get(bodyId=str(bodyId))
		body_delete.delete()
		return HttpResponse(status=204)

@csrf_exempt
def post_list(request):
	if request.method == 'GET':
		post = Post.objects.all()
		user = Users.objects.all()
		category = Categories.objects.all()

		post_json = {}
		post_record = []

		post_serializer = PostsSerializer(post, many=True)
		user_serializer = UserSerializer(user, many=True)
		category_serializer = CategorySerializer(category, many=True)
		
		for post_data in post_serializer.data:
			for user_data in user_serializer.data:
				for category_data in category_serializer.data:
					if (str(post_data.get('userId')).strip() == str(user_data.get('userId')).strip()) and (str(post_data.get('categoryId')).strip() == str(category_data.get('categoryId')).strip()):
						id = post_data.get('postId')
						name = post_data.get('name')
						description = post_data.get('description')
						mainImg = post_data.get('mainImg')
						createAt = post_data.get('createAt')
						userId = user_data.get('userId')
						userName = user_data.get('userName')
						avatar = user_data.get('avatar')
						categoryId = category_data.get('categoryId')
						categoryName = category_data.get('categoryName')
						record_category = {'categoryId':categoryId , 'categoryName': categoryName}
						record_user = {'userId': userId , 'userName': userName , 'avatar': avatar}
						record = {'postId': id, 'name': name, 'description': description, 'mainImg': mainImg, 'author': record_user , 'category': record_category,'createAt': createAt}
						post_record.append(record)

						print("get success")
						break
		post_json = post_record
		return JsonResponse(post_json , safe=False)
	
	elif request.method == 'POST':
		try:
			post_data = JSONParser().parse(request)[0]
			body_result = []
			body_data = post_data['body']
			# print("Body data :",body_data)
			post_serializer = PostsSerializer(data=post_data)
			if post_serializer.is_valid():
				post_serializer.save()
			for body in body_data:
				body['postId'] = post_serializer.data.get('postId').strip()
				body_result.append(body)
				print(post_serializer.data['postId'])
				body_serializer_add = BodySerializer(data=body)
				if body_serializer_add.is_valid():
					print("saved")
					body_serializer_add.save()
				print(body)
			
			return JsonResponse(post_serializer.data, status=201)
		except Exception as e:
			print("Error :",e)
			return HttpResponse(status=400)
		

@csrf_exempt
def post_detail(request, postId):
	try:
		post = Post.objects.all()
		user = Users.objects.all()
		category = Categories.objects.all()
		body = Body.objects.all()
		post_serializer = PostsSerializer(post , many = True)
		user_serializer = UserSerializer(user,many = True)
		category_serializer = CategorySerializer(category , many = True)
		body_serializer = BodySerializer(body, many = True)
	except post.DoesNotExist:
		return HttpResponse(status=404)
	if request.method == 'GET':

		post_json = {}
		post_record = []
		body_record = []
		for body_data in body_serializer.data:
			for post_data in post_serializer.data:
						if str(post_data.get('postId')).strip() == str(postId).strip() and str(body_data.get('postId')).strip() == str(postId).strip():
							bodyId = body_data.get('bodyId')
							content = body_data.get('content')
							image = body_data.get('imageBody')
							tittle = body_data.get('tittleBody')
							record_body = {'bodyId': bodyId , 'content': content , 'imageBody': image , 'tittleBody': tittle}
							body_record.append(record_body)
							break
		# loop post
		for post_data in post_serializer.data:
			# check postId
			if str(post_data.get('postId')).strip() == str(postId).strip():
				for user_data in user_serializer.data:
					for category_data in category_serializer.data:
						if (str(post_data.get('userId')).strip() == str(user_data.get('userId')).strip()) and (str(post_data.get('categoryId')).strip() == str(category_data.get('categoryId')).strip()):
							postId = post_data.get('postId')
							name = post_data.get('name')
							description = post_data.get('description')
							mainImg = post_data.get('mainImg')
							createAt = post_data.get('createAt')
							userId = user_data.get('userId')
							userName = user_data.get('userName')
							avatar = user_data.get('avatar')
							categoryId = category_data.get('categoryId')
							categoryName = category_data.get('categoryName')
							record_category = {'categoryId':categoryId , 'categoryName': categoryName}
							record_user = {'userId': userId , 'userName': userName , 'avatar': avatar}
							record = {'postId':postId, 'name': name, 'description': description, 'mainImg': mainImg, 'author': record_user , 'category': record_category,'createAt': createAt , 'body': body_record}
							post_record.append(record)

							print("get success")
							break
		
		return JsonResponse(post_record , safe=False)

	elif request.method == 'PUT':
		try:
			post_data = JSONParser().parse(request) # post_data from request
			post_update = Post.objects.get(postId=postId) # 
			body_update = post_data['body']
			# print(body_update)
			body = Body.objects.all()
			body_data = post_data['body']
			categoryId = post_data['category']['categoryId']
			userId = post_data['author']['userId']
			name = post_data['name']
			description = post_data['description']
			mainImg = post_data['mainImg']
			createAt = post_data['createAt']
			post_data_update = {'postId': postId, 'name': name, 'description': description, 'mainImg': mainImg, 'userId': userId , 'categoryId': categoryId,'createAt': createAt}
			post_serializer = PostsSerializer(post_update, data=post_data_update)
			# body_serializer = BodySerializer(data=body_data)
			body_serializer_all = BodySerializer(body, many=True)
			for body_data_all in body_serializer_all.data:
				if body_data_all['postId'] == postId:
					body_data_all = Body.objects.get(bodyId=body_data_all['bodyId'])
					# print(body_data_all)
					body_data_all.delete()
					# body_serializer.delete()
					break
			
			if post_serializer.is_valid():
				post_serializer.save()
			for body in body_data:
				body_serializer_add = BodySerializer(data=body)
				if body_serializer_add.is_valid():
					print("saved")
					body_serializer_add.save()
				print(body)
				# body_serializer.save()
			return JsonResponse("OK" , status=201 , safe=False)
		except Exception as e:
			print("Error :",e )
			return HttpResponse(status=400)
	elif request.method == 'DELETE':
		post_delete = Post.objects.get(postId=postId)
		post_delete.delete()
		return HttpResponse(status=204)


@csrf_exempt
def login(request):
	user_login = []
	if request.method == 'POST':
		print(token)
		data = JSONParser().parse(request)
		username = data['userName'].strip()
		password = data['passWord'].strip()
		try:
			user = Users.objects.get(userName=username)
			if user.passWord == password:
				user_serializer = UserSerializer(user)
				result = {"user":user_serializer.data,"token":token}
				user_login.append(result)
				return JsonResponse(user_login , status=201 , safe=False)
			else:
				return JsonResponse({'message': 'password is incorrect'}, status=400 , safe=False)
		except Users.DoesNotExist:
			return JsonResponse({'message': 'user is not exist'}, status=400 , safe=False)
	elif request.method == 'GET':
		# print(token)

		return JsonResponse({'message': 'logout success'} , status=201 , safe=False)
