from django.forms import widgets
from rest_framework import serializers
from wildfire.models import User, Question, Answer, GENDER_CHOICES, QUESTION_TYPE_CHOICE

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
		user.pasword = validated_data['password']
		user.save()
		return user

class QuestionSerializer(serializers.ModelSerializer):
	asker = UserSerializer(many=False)
	categories = serializers.StringRelatedField(many=True, read_only=True)

	class Meta:
		model = Question
		fields = ('id', 'text', 'question_type', 'date', 'asker', 'categories', 'option1', 'option2', 'option3', 'option4', 'option5')
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
		question_type = data.get('question_type')

		if options:
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
	asker = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

	class Meta:
		model = Question
		fields = ('id', 'text', 'question_type', 'date', 'asker', 'option1', 'option2', 'option3', 'option4', 'option5')
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
		question_type = data.get('question_type')

		if options:
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
		
class AnswerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Answer
		fields = ('id', 'user', 'question', 'answer')
		read_only_fields = ('id')

class CreateAnswerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Annswer
		fields = ('id', 'user', 'question', 'answer')
		read_only_fields = ('id')
	
	def create(self, validated_data):
		answer = Answer(
			user = validated_data['user'],
			question = validated_data['question'],
			answer = validated_data['answer']
		)
		answer.save()
		return answer