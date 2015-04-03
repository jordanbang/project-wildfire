from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
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
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import TokenAuthentication

from wildfire.models import UserProfile, Question, Answer, Connected, TargetedQuestion, Category
from wildfire.serializers import UserSerializer, UserProfileSerializer, QuestionSerializer
from wildfire.serializers import AnswerSerializer, StatsSerializer, ConnectionSerializer
from wildfire.permissions import isOwnerOrReadOnly

from wildfire.targeted_question_helper import target_from_answer, target_from_question
from wildfire.question_helper import get_news_for_question

# Create your views here.
class JSONResponse(HttpResponse):
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

#Helper functions
#Call this function before returning a json response
def add_user(data, request):
	user = request.user
	if not user.is_anonymous():
		print("User is authenticated " + request.user.username)
		user_data = UserProfileSerializer(user.profile).data
	else:
		print("User is not authenticated")
		user_data = None
	
	ret = dict()
	ret['user'] = user_data
	ret['response'] = data
	return ret
	

# /user Endpoints
@api_view(['GET'])
@csrf_exempt
#@permission_classes((IsAuthenticated,))
def user_list(request):
	print(request.user)
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
#@permission_classes((isOwnerOrReadOnly, IsAuthenticatedOrReadOnly))
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
@api_view(['GET'])
def question_list(request):
	print(request.user)

	# print("Request has auth header: " + str(request.has_header("Authorization")))
	# print(request.auth)
	if request.method == 'GET':
		ret = dict()
		user = request.user
		usersQuestions = None
		if user.is_anonymous():
			ret['usersQuestions'] = [];
		else:
			usersQuestions = TargetedQuestion.objects.filter(user=user.profile).values_list('question', flat=True)
			userQuestionObj = Question.objects.filter(id__in=usersQuestions)
			userQuestions_serializer = QuestionSerializer(userQuestionObj, many=True, context={'request':request})
			ret['userQuestions'] = userQuestions_serializer.data			

		questions = Question.objects.all().order_by('-date').exclude(id__in=[18])
		# if usersQuestions:
		# 	questions = Question.objects.all().order_by('-date').exclude(id__in=usersQuestions)	
		serializer = QuestionSerializer(questions, many=True, context={'request':request})
		ret['popularQuestions'] = serializer.data
		return JSONResponse(add_user(ret, request))

@csrf_exempt
@api_view(['GET'])
def question_detail(request, pk):
	try:
		question = Question.objects.get(pk=pk)
	except Question.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = QuestionSerializer(question, context={'request':request})
		return JSONResponse(add_user(serializer.data, request))

@csrf_exempt
@api_view(['POST'])	
#@permission_classes((isOwnerOrReadOnly, IsAuthenticatedOrReadOnly))	
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
@api_view(['POST'])
def question_create(request):
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = QuestionSerializer(data=data, context={'request':request})
		if serializer.is_valid():
			new_question = serializer.save()
			target_from_question(new_question)
			get_news_for_question(new_question)
			return JSONResponse(add_user(serializer.data, request))
		return JSONResponse(serializer.errors, status=400)

@csrf_exempt
@api_view(['GET'])		
#/answers endpoints
def answer_list(request):
	if request.method == 'GET':
		answers = Answer.objects.all()
		serializer = AnswerSerializer(answers, many=True)
		return JSONResponse(add_user(serializer.data, request))

@csrf_exempt
@api_view(['GET'])		
def answer_detail(request, pk):
	try:
		answer = Answer.objects.get(pk=pk)
	except Answer.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = AnswerSerializer(answer)
		return JSONResponse(add_user(serializer.data, request))

@csrf_exempt
@api_view(['POST'])
#@permission_classes((isOwnerOrReadOnly))
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
@api_view(['POST'])		
def answer_create(request):
	if request.method =='POST':
		data = JSONParser().parse(request)
		serializer = AnswerSerializer(data=data)
		if serializer.is_valid():
			answer = serializer.save()
			questionSerializer = QuestionSerializer(answer.question, context={'request':request})
			target_from_answer(answer)
			return JSONResponse(add_user(questionSerializer.data, request))
		return JSONResponse(serializer.errors, status=400)

#/stats endpoints
@csrf_exempt
@api_view(['GET'])
def stats(request, pk):
	try:
		question = Question.objects.get(pk=pk)
	except Question.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = StatsSerializer(question)
		return JSONResponse(add_user(serializer.data, request))


class GetAuthToken(ObtainAuthToken):
	def post(self, request):
		serializer = AuthTokenSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.validated_data['user']
			token, created = Token.objects.get_or_create(user=user)
			
			data = UserProfileSerializer(user.profile).data
			data['token'] = token.key
			return JSONResponse(data)
		return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def wild_logout(request):
	logout(request)
	return JSONResponse({})



#/profile endpoint
@api_view(['GET'])
@csrf_exempt
#@permission_classes((IsAuthenticated,))
def profile(request, pk):
	try:
		user = UserProfile.objects.get(pk=pk)
	except UserProfile.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		user_data = UserProfileSerializer(user).data

		users_questions = Question.objects.filter(asker=user)
		questions_data = QuestionSerializer(users_questions, many=True).data
		users_answers = Answer.objects.filter(user=user)
		answers_data = AnswerSerializer(users_answers, many=True).data		

		connections1 = Connected.objects.filter(user1=user).values_list('user2', flat=True) 
		connections_as_user = UserProfile.objects.filter(id__in=connections1)
		connections_data = UserProfileSerializer(connections_as_user, many=True).data

		ret = dict()
		ret['user'] = user_data
		ret['questions'] = questions_data
		ret['connections'] = connections_data
		ret['numQuestionsAsked'] = Question.objects.filter(asker=user).count()
		ret['numQuestionsAnswered'] = Answer.objects.filter(user=user).count()
		ret['numConnections'] = Connected.objects.filter(user1=user).count()
		ret['answers'] = answers_data
		return JSONResponse(add_user(ret, request))

@api_view(['POST'])
@csrf_exempt
def connect(request):
	data = JSONParser().parse(request)
	serializer = ConnectionSerializer(data=data)
	if serializer.is_valid():
		connection = serializer.save()
		return JSONResponse(add_user(serializer.data, request))
	return JSONResponse(serializer.errors, status=400)


@api_view(['GET'])
@csrf_exempt
def search(request):
	search_term = request.GET.get('q', None)
	if search_term:
		ret = dict()

		users_name = User.objects.filter(username__icontains=search_term)
		user_first = User.objects.filter(first_name__icontains=search_term)
		user_last = User.objects.filter(last_name__icontains=search_term)
		user = (users_name | user_first| user_last).distinct('id')
		user_profiles = UserProfile.objects.filter(user__in=user)
		print("Search return " + str(user_profiles.count()) +  " users")


		questions_text = Question.objects.filter(text__icontains=search_term)
		categories_text = Category.objects.filter(category__icontains=search_term)
		questions_cat = Question.objects.filter(categories__in=categories_text)
		question_asker = Question.objects.filter(asker__in=user_profiles)
		question_return_set = (questions_text | questions_cat | question_asker).distinct('id')

		print("Search return " + str(question_return_set.count()) + " questions")
		
		serializer = UserProfileSerializer(user_profiles, many=True)
		ret['users'] = serializer.data
		serializer = QuestionSerializer(question_return_set, many=True, context={'request':request})
		ret['questions'] = serializer.data
		

		return JSONResponse(add_user(ret, request))
	return JSONResponse(serializer.errors, status=400)

#/stats endpoints
@csrf_exempt
@api_view(['GET'])
def replies(request, pk):
	try:
		question = Question.objects.get(pk=pk)
	except Question.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		replies = Question.objects.filter(replyTo=pk)
		serializer = QuestionSerializer(replies, many=True, context={'request':request})
		return JSONResponse(add_user(serializer.data, request))