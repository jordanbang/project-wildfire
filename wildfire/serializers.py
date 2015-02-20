from django.forms import widgets
from django.contrib.auth.models import User

from rest_framework import serializers

from wildfire.models import UserProfile, Question, Answer
from wildfire.models import GENDER_CHOICES, QUESTION_TYPE_CHOICE


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
	password = serializers.CharField(source='user.password', write_only=True)
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
	categories = serializers.StringRelatedField(many=True, read_only=True)
	answers = AnswerSerializer(many=True, read_only=True)

	class Meta:
		model = Question
		fields = ('id', 'text', 'questionType', 'date', 'asker', 'categories', 
			'option1', 'option2', 'option3', 'option4', 'option5', 'answers')
		read_only_fields = ('id', 'date')

	def to_representation(self, obj):
		rep = super(serializers.ModelSerializer, self).to_representation(obj)
		
		options = []
		for i in xrange(1,6):
			option = rep.pop('option' + str(i))
			if option:
				options.append(option)

		rep['options'] = options

		#For now, always assume that the person requesting info is a (validated) user
		rep['isUser'] = True

		#For now, isAnswered will be a global field, just returning if the question has been answered.
		answers = rep['answers']
		rep['isAnswered'] = len(answers) > 0


		return rep

	def to_internal_value(self, data):
		options = data.pop('options', None)
		if options and 'questionType' in data:
			question_type = data.get('questionType')
			# Need to update the options for either multiple choice or range values
			if question_type == 'MC' or question_type == 'RG':
				for i in xrange(0,5):
					if i < len(options) and options[i]:
						data['option' + str(i+1)] = options[i]
					else:
						data['option' + str(i+1)] = ""
			elif question_type == 'TF':
				data['option1'] = 'True'
				data['option2'] = 'False'
			elif question_type == 'RA':
				for i in xrange(1,6):
					data['option' + str(i)] = options[i-1]			
		return super(serializers.ModelSerializer, self).to_internal_value(data)

class CreateQuestionSerializer(serializers.ModelSerializer):
	asker = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())

	class Meta:
		model = Question
		fields = ('id', 'text', 'questionType', 'date', 'asker', 'option1', 'option2', 'option3', 'option4', 'option5')
		read_only_fields = ('id', 'date')

	def to_representation(self, obj):
		rep = super(serializers.ModelSerializer, self).to_representation(obj)
		
		options = []
		for i in xrange(1,6):
			option = rep.pop('option' + str(i))
			if option:
				options.append(option)

		rep['options'] = options
		return rep

	def to_internal_value(self, data):
		options = data.pop('options', None)
		if options and 'questionType' in data:
			question_type = data.get('questionType')
			# Need to update the options for either multiple choice or range values
			if question_type == 'MC' or question_type == 'RG':
				for i in xrange(0,5):
					if i < len(options) and options[i]:
						data['option' + str(i+1)] = options[i]
					else:
						data['option' + str(i+1)] = ""
			elif question_type == 'TF':
				data['option1'] = 'True'
				data['option2'] = 'False'
			elif question_type == 'RA':
				for i in xrange(1,6):
					data['option' + str(i)] = options[i-1]			
		return super(serializers.ModelSerializer, self).to_internal_value(data)
	
