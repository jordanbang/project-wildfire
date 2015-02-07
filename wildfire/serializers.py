from django.forms import widgets
from rest_framework import serializers
from wildfire.models import User, Question, GENDER_CHOICES

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


class QuestionSerializer(serializers.ModelSerializer):
	asker = UserSerializer(many=False, read_only=True)

	class Meta:
		model = Question
		fields = ('id', 'text', 'question_type', 'date', 'asker')