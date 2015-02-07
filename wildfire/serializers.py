from django.forms import widgets
from rest_framework import serializers
from wildfire.models import User, Question, GENDER_CHOICES

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'age', 'gender', 'region', 'join_date')


class QuestionSerializer(serializers.ModelSerializer):
	asker = UserSerializer(many=False, read_only=True)

	class Meta:
		model = Question
		fields = ('id', 'text', 'question_type', 'date', 'asker')