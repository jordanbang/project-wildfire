from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import permissions

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
@login_required
def user_list(request):
	if request.method == 'GET':
		users = UserProfile.objects.all()
		serializer = UserProfileSerializer(users, many=True)

		if request.user.is_authenticated():
			print("User is authenticated " + request.user.username)
		else:
			print("User is not authenticated")

		return JSONResponse(serializer.data)

@csrf_exempt
@login_required
def user_detail(request, pk):
	try:
		user = UserProfile.objects.get(pk=pk)
		print("User id:" + str(user.user.id))
		print("User profile id: " + str(user.id))
	except UserProfile.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = UserProfileSerializer(user)
		return JSONResponse(serializer.data)

@csrf_exempt
@login_required
def user_update(request, pk):
	try:
		userProfile = UserProfile.objects.get(pk=pk)
		user = userProfile.user
	except UserProfile.DoesNotExist:
		return HttpResponse(status=404)


	if request.method == 'POST':
		data = JSONParser().parse(request)
		userProfileSerializer = UserProfileSerializer(userProfile, data=data, partial=True)
		userSerializer = UserSerializer(user, data=data, partial=True)
		if userProfileSerializer.is_valid() and userSerializer.is_valid():
			userSerializer.save()
			userProfileSerializer.save()
			return JSONResponse(userProfileSerializer.data)
		errors = dict()
		errors.update(userProfileSerializer.errors)
		errors.update(userSerializer.errors)
		return JSONResponse(errors, status=400)

@csrf_exempt
@login_required
def user_create(request):
	if request.method == 'POST':
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
		questions = Question.objects.all()
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