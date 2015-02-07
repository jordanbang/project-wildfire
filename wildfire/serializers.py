from django.forms import widgets
from rest_framework import serializers
from wildfire.models import User, Question, MultipleChoiceOption, RangeOption, GENDER_CHOICES, QUESTION_TYPE_CHOICE

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'age', 'gender', 'region', 'join_date')
		read_only_fields = ('id', 'join_date')

class CreateUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'password', 'age', 'gender', 'region', 'join_date')
		read_only_fields = ('id', 'join_date')
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		user = User(
			username = validated_data['username'],
			age = validated_data['age'],
			gender = validated_data['gender'],
			region = validated_data['region']
		)
		user.set_password(validated_data['password'])
		user.save()
		return user

class RangeOptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = RangeOption
		fields = ('lower_bound', 'upper_bound')

class MultipleChoiceOptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = MultipleChoiceOption
		fields = ('choice1', 'choice2', 'choice3', 'choice4', 'choice5')

	# def to_representation(self, obj):

	# 	return "hi";

	# def to_internal_value(self, data):
	# 	# take the data, and create validated data that can then be passed to MultipleChoiceOption to be turned into a model
	# 	return

class QuestionSerializer(serializers.ModelSerializer):
	asker = UserSerializer(many=False, read_only=True)
	multiple_choice_options = MultipleChoiceOptionSerializer(many=False, read_only=True)
	range_options = RangeOptionSerializer(many=False, read_only=True) 

	class Meta:
		model = Question
		fields = ('id', 'text', 'question_type', 'date', 'asker', 'multiple_choice_options', 'range_options')

	def to_representation(self, obj):
		rep = super(serializers.ModelSerializer, self).to_representation(obj)
		
		mc_options = rep.pop('multiple_choice_options', None)
		range_options = rep.pop('range_options')

		options = []
		question_type = rep['question_type']
		if question_type == 'MC':
			for i in mc_options:
				option = mc_options[i]
				if option:
					options.append(option)
		elif question_type == 'RG':
			for i in range_options:
				options.append(range_options[i])
		elif question_type == 'TF':
			options.append('True')
			options.append('False')
		elif question_type == 'RA':
			options.append('5')

		rep['options'] = options
		return rep