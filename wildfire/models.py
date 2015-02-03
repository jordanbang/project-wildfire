from django.db import models

GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'),)
# Create your models here.
class User(models.Model):
	username = models.CharField(max_length = 20)
	password = models.CharField(max_length = 20)
	age = models.IntegerField()
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
	region = models.CharField(max_length = 20)
	join_date = models.DateTimeField()
	

class Question(models.Model):
	user = models.ForeignKey(User)
	id = models.IntegerField(primary_key = True)
	text = models.CharField(max_length = 200)
	type = models.CharField(max_length = 20)
	date = models.DateTimeField()
	
class Category(models.Model):
	question = models.ManyToManyField(Question)
	category = models.CharField(max_length = 20)

class MultipleChoiceOption(models.Model):
	choice1 = models.CharField(max_length = 40)
	choice2 = models.CharField(max_length = 40)
	choice3 = models.CharField(max_length = 40)
	choice4 = models.CharField(max_length = 40)
	choice5 = models.CharField(max_length = 40)

class RangeOption(models.Model):
	lower_bound = models.IntegerField(default = 0) 
	upper_bound = models.IntegerField(default = 100)

class Answer(models.Model):
	user = models.ForeignKey(User)
	question = models.ForeignKey(Question)
	answer = models.IntegerField()