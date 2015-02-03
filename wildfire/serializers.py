from django.forms import widgets
from rest_framework import serializers
from wildfire.models import User, GENDER_CHOICES

# class UserSerializer(serializers.Serializer):
# 	pk = serializers.IntegerField(read_only=True)
# 	username = serializers.CharField(required=True, allow_blank=False, max_length=100)
# 	password = serializers.CharField(max_length=20)
# 	age = serializers.IntegerField(required=True)
# 	gender = serializers.ChoiceField(choices=GENDER_CHOICES, default='M', allow_blank=False)
# 	region = serializers.CharField(required=True, allow_blank=True, max_length=20)
# 	join_date = serializers.DateTimeField()

# 	def create(self, validated_data):
# 		return User.objects.create(**validated_data)

# 	def update(self, instance, validated_data):
# 		instance.username = validated_data.get('username', instance.username)
# 		instance.age = validated_data.get('age', instance.age)
# 		instance.gender = validated_data.get('gender', instance.gender)
# 		instance.region = validated_data.get('region', instance.region)
# 		instance.password = validated_data.get('password', instance.password)
# 		instance.save()
# 		return instance

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'age', 'gender', 'region', 'join_date')