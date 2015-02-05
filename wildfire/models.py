from django.db import models

# Create your models here.
class User(models.Model):
	id = models.IntegerField(primary_key = True)
	username = models.CharField(max_length = 20)
	password = models.CharField(max_length = 20)
	age = models.IntegerField()
	# we should look at this.  Gender true or false?
	gender = models.BooleanField()
	region = models.CharField(max_length = 20)
	join_date = models.DateTimeField()
	

class Question(models.Model):
	user = models.ForeignKey(User)
	id = models.IntegerField(primary_key = True)
	text = models.CharField(max_length = 200)
	type = models.CharField(max_length = 20)
	date = models.DateTimeField()
	
class Categories(models.Model):
	question = models.ManyToManyField(Question)
	category = models.CharField(max_length = 20)

class MultipleChoiceOptions(models.Model):
	choice1 = models.CharField(max_length = 40)
	choice2 = models.CharField(max_length = 40)
	choice3 = models.CharField(max_length = 40)
	choice4 = models.CharField(max_length = 40)
	choice5 = models.CharField(max_length = 40)

class RangeOptions(models.Model):
	lower_bound = models.IntegerField(default = 0) 
	upper_bound = models.IntegerField(default = 100)

class Answers(models.Model):
	user = models.ForeignKey(User)
	question = models.ForeignKey(Question)
	answer = models.IntegerField()