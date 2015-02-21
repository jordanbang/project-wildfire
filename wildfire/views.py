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

from wildfire.models import UserProfile, Question, Answer
from wildfire.serializers import UserSerializer, UserProfileSerializer, QuestionSerializer
from wildfire.serializers import CreateQuestionSerializer
from wildfire.serializers import AnswerSerializer

# Create your views here.
class JSONResponse(HttpResponse):
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

# /user Endpoints
@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def user_list(request):
	if request.method == 'GET':
		users = UserProfile.objects.all()
		if request.user.is_authenticated():
			print("User is authenticated " + request.user.username)
		else:
			print("User is not authenticated")
		serializer = UserProfileSerializer(users, many=True)
		return Response(serializer.data)

@csrf_exempt
@api_view(['GET', 'POST'])
def user_detail(request, pk):
	try:
		user = UserProfile.objects.get(pk=pk)
	except UserProfile.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = UserProfileSerializer(user)
		return Response(serializer.data)
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		userProfileSerializer = UserProfileSerializer(userProfile, data=data, partial=True)
		userSerializer = UserSerializer(user, data=data, partial=True)
		if userProfileSerializer.is_valid() and userSerializer.is_valid():
			userSerializer.save()
			userProfileSerializer.save()
			return Response(userProfileSerializer.data)
		errors = dict()
		errors.update(userProfileSerializer.errors)
		errors.update(userSerializer.errors)
		return Response(errors, status=status.HTTP_400_NOT_FOUND)
		

@csrf_exempt
@api_view(['GET'])
@login_required
def user_create(request):
	data = JSONParser().parse(request)
	errors = dict()
	userSerializer = UserSerializer(data=data)
	if userSerializer.is_valid():
		new_user = userSerializer.save()
		userProfileSerializer = UserProfileSerializer(new_user.profile, data=data, partial=True)
		
		if userProfileSerializer.is_valid():
			userProfileSerializer.save()
		return JSONResponse(userProfileSerializer.data)
		errors.update(userProfileSerializer.errors)
	else:
		errors.update(userSerializer.errors)
	return JSONResponse(errors, status=400)


# /question Endpoints
@csrf_exempt
def question_list(request):
	if request.method == 'GET':
		questions = Question.objects.all().order_by('-date')
		serializer = QuestionSerializer(questions, many=True)
		return JSONResponse(serializer.data)

@csrf_exempt
def question_detail(request, pk):
	try:
		question = Question.objects.get(pk=pk)
	except Question.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = QuestionSerializer(question)
		return JSONResponse(serializer.data)
	
@csrf_exempt
def question_update(request, pk):
	try:
		question = Question.objects.get(pk=pk)
	except Question.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = QuestionSerializer(question, data=data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data)
		return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def question_create(request):
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = CreateQuestionSerializer(data=data)
		if serializer.is_valid():
			new_question = serializer.save()
			return JSONResponse(QuestionSerializer(new_question).data)
		return JSONResponse(serializer.errors, status=400)

#/answers endpoints
@csrf_exempt
def answer_list(request):
	if request.method == 'GET':
		answers = Answer.objects.all()
		serializer = AnswerSerializer(answers, many=True)
		return JSONResponse(serializer.data)

@csrf_exempt		
def answer_detail(request, pk):
	try:
		answer = Answer.objects.get(pk=pk)
	except Answer.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = AnswerSerializer(answer)
		return JSONResponse(serializer.data)

@csrf_exempt
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
			return JSONResponse(serializer.data)
		return JSONResponse(serializer.errors, status=400)
		
@csrf_exempt
def answer_create(request):
	if request.method =='POST':
		data = JSONParser().parse(request)
		serializer = AnswerSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data)
		return JSONResponse(serializer.errors, status=400)


# @api_view(['GET'])
# @authentication_classes((SessionAuthentication,))
# def example_view(request):
# 	content = {
# 		'user':unicode(request.user),
# 		'auth':unicode(request.auth),
# 	}
# 	return Response(content)



class AuthView(APIView):
	def post(self, request, *args, **kwargs):
		auth_user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if auth_user is not None:
			if auth_user.is_active:
				login(request, auth_user)
				return Response(UserSerializer(auth_user).data)
			else:
				return Response(status=403)
		return Response(status=404)

	def delete(self, request, *args, **kwargs):
		logout(request)
		return Response({})