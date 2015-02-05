from django.db import models

# Create your models here.
class User(models.model):
	id = models.IntegerField(primary_key = True)
	username = models.CharField(max_length = 20)
	password = models.CharField(max_length = 20)
	age = models.IntegerField()
	gender = models.BooleanField()
	region = models.CharField(max_length = 20)
	join_date = models.DateTimeField()
	

class Question(models.model):
	user = models.ForeignKey(User)
	id = models.IntegerField(primary_key = True)
	text = models.CharField(max_length = 200)
	type = models.CharField(max_length = 20)
	date = models.DateTimeField()
	
class Categories(models.model):
	question = models.ManyToManyField(Question)
	category = models.CharField(max_length = 20)

class MultipleChoiceOptions(models.model):
	choice1 = models.CharField(max_length = 40)
	choice2 = models.CharField(max_length = 40)
	choice3 = models.CharField(max_length = 40)
	choice4 = models.CharField(max_length = 40)
	choice5 = models.CharField(max_length = 40)

class RangeOptions(models.model):
	lower_bound = models.IntegerField(default = 0) 
	upper_bound = models.IntegerFiled(default = 100)

class Answers(models.model):
	user = models.ForeignKey(User)
	question = models.ForeignKey(Question)
	answer = models.IntegerField()