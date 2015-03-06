from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication

from wildfire.models import UserProfile, Question, Answer, Connected
from wildfire.serializers import UserSerializer, UserProfileSerializer, QuestionSerializer
from wildfire.serializers import AnswerSerializer, StatsSerializer, ConnectionSerializer
from wildfire.permissions import isOwnerOrReadOnly

# Create your views here.
class JSONResponse(HttpResponse):
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

#Helper functions
def add_user(data, request):
	user = request.user
	if user:
		user_data = UserProfileSerializer(user.profile).data
	else:
		user_data = "Anonymous"
	
	ret = dict()
	ret['user'] = user_data
	ret['response'] = data
	return ret
	

# /user Endpoints
@api_view(['GET'])
@csrf_exempt
@permission_classes((IsAuthenticated,))
def user_list(request):
	if request.method == 'GET':
		users = UserProfile.objects.all()
		if request.user.is_authenticated():
			print("User is authenticated " + request.user.username)
		else:
			print("User is not authenticated")
		serializer = UserProfileSerializer(users, many=True)
		return Response(add_user(serializer.data, request))

@api_view(['GET', 'POST'])
@csrf_exempt
@permission_classes((isOwnerOrReadOnly, IsAuthenticatedOrReadOnly))
def user_detail(request, pk):
	try:
		user = UserProfile.objects.get(pk=pk)
	except UserProfile.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = UserProfileSerializer(user)
		return Response(add_user(serializer.data, request))
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		userProfileSerializer = UserProfileSerializer(userProfile, data=data, partial=True)
		userSerializer = UserSerializer(user, data=data, partial=True)
		if userProfileSerializer.is_valid() and userSerializer.is_valid():
			userSerializer.save()
			userProfileSerializer.save()
			return Response(add_user(userProfileSerializer.data,request))
		errors = dict()
		errors.update(userProfileSerializer.errors)
		errors.update(userSerializer.errors)
		return Response(errors, status=status.HTTP_400_NOT_FOUND)
		
@api_view(['POST'])
@csrf_exempt
def user_create(request):
	data = JSONParser().parse(request)
	errors = dict()
	userSerializer = UserSerializer(data=data)
	if userSerializer.is_valid():
		new_user = userSerializer.save()
		userProfileSerializer = UserProfileSerializer(new_user.profile, data=data, partial=True)
		
		if userProfileSerializer.is_valid():
			userProfileSerializer.save()

		#TODO: should log the user in at this point
		return JSONResponse(add_user(userProfileSerializer.data, request))
		errors.update(userProfileSerializer.errors)
	else:
		errors.update(userSerializer.errors)
	return JSONResponse(errors, status=400)


# /question Endpoints
@csrf_exempt
def question_list(request):
	if request.method == 'GET':
		questions = Question.objects.all().order_by('-date')
		serializer = QuestionSerializer(questions, many=True, context={'request':request})
		return JSONResponse(add_user(serializer.data, request))

@csrf_exempt
def question_detail(request, pk):
	try:
		question = Question.objects.get(pk=pk)
	except Question.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = QuestionSerializer(question, context={'request':request})
		return JSONResponse(add_user(serializer.data, request))

@csrf_exempt	
@permission_classes((isOwnerOrReadOnly, IsAuthenticatedOrReadOnly))	
def question_update(request, pk):
	try:
		question = Question.objects.get(pk=pk)
	except Question.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = QuestionSerializer(question, data=data, partial=True, context={'request':request})
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(add_user(serializer.data, request))
		return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def question_create(request):
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = QuestionSerializer(data=data, context={'request':request})
		if serializer.is_valid():
			new_question = serializer.save()
			return JSONResponse(add_user(serializer.data, request))
		return JSONResponse(serializer.errors, status=400)

@csrf_exempt		
#/answers endpoints
def answer_list(request):
	if request.method == 'GET':
		answers = Answer.objects.all()
		serializer = AnswerSerializer(answers, many=True)
		return JSONResponse(add_user(serializer.data, request))

@csrf_exempt		
def answer_detail(request, pk):
	try:
		answer = Answer.objects.get(pk=pk)
	except Answer.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = AnswerSerializer(answer)
		return JSONResponse(add_user(serializer.data, request))

@csrf_exempt
@permission_classes((isOwnerOrReadOnly))
def answer_update(request, pk):
	try:
		answer = Answer.objects.get(pk=pk)
	except Answer.DoesNotExist:
		return HttpResponse(status=404)
	
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = AnswerSerializer(answer, data=data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(add_user(serializer.data, request))
		return JSONResponse(serializer.errors, status=400)

@csrf_exempt		
def answer_create(request):
	if request.method =='POST':
		data = JSONParser().parse(request)
		serializer = AnswerSerializer(data=data)
		if serializer.is_valid():
			answer = serializer.save()
			questionSerializer = QuestionSerializer(answer.question, context={'request':request})
			return JSONResponse(add_user(questionSerializer.data, request))
		return JSONResponse(serializer.errors, status=400)

#/stats endpoints
@csrf_exempt
def stats(request, pk):
	try:
		question = Question.objects.get(pk=pk)
	except Question.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = StatsSerializer(question)
		return JSONResponse(add_user(serializer.data, request))


#user login and logout
@csrf_exempt
def wild_login(request):
	auth_user = authenticate(username=request.POST['username'], password=request.POST['password'])
	if auth_user is not None:
		if auth_user.is_active:
			login(request, auth_user)
			return JSONResponse(UserProfileSerializer(auth_user.profile).data)
		else:
			return JSONResponse({"error":"User is not active"}, status=403)
	return JSONResponse({"error":"User not found"}, status=404)

@csrf_exempt
def wild_logout(request):
	logout(request)
	return JSONResponse({})



#/profile endpoint

#Have to be logged in to view profile
#Profile will return the user information (in the outer user object), their questions
#(in the inner response object) and their connections (in the inner response object)

@csrf_exempt
@permission_classes((IsAuthenticated,))
def profile(request):
	try:
		user = request.user.profile
	except UserProfile.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		users_questions = Question.objects.filter(asker=user)
		questions_data = QuestionSerializer(users_questions, many=True).data

		connections = Connected.objects.filter(user1=user) | Connected.objects.filter(user2=user)
		connections_data = ConnectionSerializer(connections, many=True, context={'user':user.id}).data

		ret = dict()
		ret['questions'] = questions_data
		ret['connections'] = connections_data

		return JSONResponse(add_user(ret, request))

