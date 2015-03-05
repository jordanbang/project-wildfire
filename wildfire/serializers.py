from django.forms import widgets
from django.contrib.auth.models import User
from django.db.models import Count

from rest_framework import serializers

from wildfire.models import UserProfile, Question, Answer, Category
from wildfire.models import GENDER_CHOICES, QUESTION_TYPE_CHOICE

from wildfire.question_serializer_helper import to_array, to_columns, get_quick_stats


class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
		read_only_fields = ('id')

	def update(self, instance, validated_data):
		instance.username = validated_data.get('username', instance.username)
		instance.email = validated_data.get('email', instance.email)
		instance.first_name = validated_data.get('first_name', instance.first_name)
		instance.last_name = validated_data.get('last_name', instance.last_name)
		if 'password' in validated_data:
			instance.set_password(validated_data['password'])	
		instance.save()
		return instance

	def create(self, validated_data):
		user = User.objects.create(**validated_data)
		user.set_password(validated_data['password'])
		user.save()
		return user

class UserProfileSerializer(serializers.ModelSerializer):
	username = serializers.CharField(source='user.username')
	email = serializers.EmailField(source='user.email')
	first_name = serializers.CharField(source='user.first_name')
	last_name = serializers.CharField(source='user.last_name')
	password = serializers.CharField(source='user.password', write_only=True, required=False)
	id = serializers.IntegerField()

	class Meta:
		model = UserProfile
		fields = ('id', 'email', 'username', 'first_name', 'last_name', 
			'age', 'gender', 'region', 'joinDate', 'avatarUrl', 'password')
		read_only_fields = ('id', 'joinDate')

	def update(self, instance, validated_data):
		instance.age = validated_data.get('age', instance.age)
		instance.gender = validated_data.get('gender', instance.gender)
		instance.region = validated_data.get('region', instance.region)
		instance.avatarUrl = validated_data.get('avatarUrl', instance.avatarUrl)
		instance.save()
		return instance

class AnswerSerializer(serializers.ModelSerializer):
	user = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
	question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())

	class Meta:
		model = Answer
		fields = ('id', 'user', 'question', 'answer')
		read_only_fields = ('id')

class QuestionSerializer(serializers.ModelSerializer):
	asker = UserProfileSerializer(many=False)
	categories = serializers.StringRelatedField(many=True, required=False)
	answers = AnswerSerializer(many=True, read_only=True)

	class Meta:
		model = Question
		fields = ('id', 'text', 'questionType', 'date', 'asker', 'categories', 
			'option1', 'option2', 'option3', 'option4', 'option5', 'answers')
		read_only_fields = ('id', 'date')

	def to_representation(self, obj):
		rep = super(serializers.ModelSerializer, self).to_representation(obj)
		rep['options'] = to_array(rep)

		#For now, isAnswered will be a global field, just returning if the question has been answered.
		answers = rep['answers']
		request = self.context.get('request', None)
		if request and request.user.is_authenticated():
			rep['isUser'] = True
			rep['user'] = request.user.first_name
			for answer in answers:
				if answer['user'] == request.user.profile.id:
					rep['isAnswered'] = True
					rep['usersAnswer'] = answer
					break
				else:
					rep['isAnswered'] = False
		else:
			rep['isUser'] = False

		answers = Answer.objects.filter(question=rep['id'])
		rep['quick'] = {
			'option1': answers.filter(answer = 0).count(),
			'option2': answers.filter(answer = 1).count(),
			'option3': answers.filter(answer = 2).count(),
			'option4': answers.filter(answer = 3).count(),
			'option5': answers.filter(answer = 4).count()
		}
		return rep

	def to_internal_value(self, data):
		asker_id = data.get('asker', None)
		if asker_id != None:
			asker = UserProfile.objects.get(pk=asker_id)
			data['asker'] = UserProfileSerializer(asker).data
		data = to_columns(data)
		categories = data.pop('categories')			
		data = super(serializers.ModelSerializer, self).to_internal_value(data)
		data['categories'] = categories
		return data

	def create(self, validated_data):
		asker = validated_data.pop('asker', None)
		if asker != None:
			asker = UserProfile.objects.get(pk=asker.pop('id'))
		question = Question.objects.create(asker=asker, **validated_data)
		question.save()
		return question


	def update(self, instance, validated_data):
		categories = validated_data.pop('categories')

		instance.text = validated_data.get('text', instance.text)
		instance.questionType = validated_data.get('questionType', instance.questionType)
		instance.option1 = validated_data.get('option1', instance.option1)
		instance.option2 = validated_data.get('option2', instance.option2)
		instance.option3 = validated_data.get('option3', instance.option3)
		instance.option4 = validated_data.get('option4', instance.option4)
		instance.option5 = validated_data.get('option5', instance.option5)
		instance.save()

		for category in categories:
			catModel = Category.objects.create(category=category)
			catModel.save()
			catModel.question.add(instance)

		return instance
		
class StatsSerializer(serializers.BaseSerializer):
	def to_representation(self, obj):
		answers = Answer.objects.filter(question=obj.pk)
		regionStats = answers.values('user__region').annotate(Count('user__region'))
		return{
			'quick':{
				'option1': answers.filter(answer = 0).count(),
				'option2': answers.filter(answer = 1).count(),
				'option3': answers.filter(answer = 2).count(),
				'option4': answers.filter(answer = 3).count(),
				'option5': answers.filter(answer = 4).count()
			},
			'male':{
				'option1': answers.filter(answer = 0,user__gender = "M").count(),
				'option2': answers.filter(answer = 1,user__gender = "M").count(),
				'option3': answers.filter(answer = 2,user__gender = "M").count(),
				'option4': answers.filter(answer = 3,user__gender = "M").count(),
				'option5': answers.filter(answer = 4,user__gender = "M").count()
			},
			'female':{
				'option1': answers.filter(answer = 0,user__gender = "F").count(),
				'option2': answers.filter(answer = 1,user__gender = "F").count(),
				'option3': answers.filter(answer = 2,user__gender = "F").count(),
				'option4': answers.filter(answer = 3,user__gender = "F").count(),
				'option5': answers.filter(answer = 4,user__gender = "F").count()
			},
			'region': regionStats
		}
