from django.db import models
from django.utils import timezone

GENDER_CHOICES = (('M', 'Male'), 
				('F', 'Female'),)

QUESTION_TYPE_CHOICE = (('MC', 'Multiple Choice'),
					('RG', 'Range'),
					('TF', 'True or False'),
					('RA', 'Rating'),)
# Create your models here.

class User(models.Model):
	username = models.CharField(max_length = 20)
	password = models.CharField(max_length = 20)
	age = models.IntegerField()
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
	region = models.CharField(max_length = 20)
	joinDate = models.DateTimeField(auto_now=True)
	avatarUrl = models.URLField(blank=True)

	def __unicode__(self):
		return self.username


class Question(models.Model):
	asker = models.ForeignKey(User)
	text = models.CharField(max_length = 200)
	questionType = models.CharField(max_length = 2, choices=QUESTION_TYPE_CHOICE)
	date = models.DateTimeField(auto_now=True)
	option1 = models.CharField(max_length = 50, blank=True)
	option2 = models.CharField(max_length = 50, blank=True)
	option3 = models.CharField(max_length = 50, blank=True)
	option4 = models.CharField(max_length = 50, blank=True)
	option5 = models.CharField(max_length = 50, blank=True)

	def __unicode__(self):
		return self.text

class Category(models.Model):
	question = models.ManyToManyField(Question, related_name='categories')
	category = models.CharField(max_length = 20)

	def __unicode__(self):
		return self.category

class Answer(models.Model):
	user = models.ForeignKey(User)
	question = models.ForeignKey(Question, related_name='answers')
	answer = models.IntegerField(default=1)