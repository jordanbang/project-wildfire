from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from wildfire.models import User, Question
from wildfire.serializers import UserSerializer, QuestionSerializer, CreateUserSerializer, CreateQuestionSerializer

# Create your views here.
class JSONResponse(HttpResponse):
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

# /user Endpoints
@csrf_exempt
def user_list(request):
	if request.method == 'GET':
		users = User.objects.all()
		serializer = UserSerializer(users, many=True)
		return JSONResponse(serializer.data)

@csrf_exempt
def user_detail(request, pk):
	try:
		user = User.objects.get(pk=pk)
	except User.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = UserSerializer(user)
		return JSONResponse(serializer.data)

@csrf_exempt
def user_update(request, pk):
	try:
		user = User.objects.get(pk=pk)
	except User.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = UserSerializer(user, data=data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data)
		return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def user_create(request):
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = CreateUserSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data)
		return JSONResponse(serializer.errors, status=400)


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
		data['question_type'] = question.question_type
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