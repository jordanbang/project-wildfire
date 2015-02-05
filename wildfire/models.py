from django.db import models

# Create your models here.
class User(models.model)
	id = models.IntegerField()
	username = models.CharField(max_length = 20)
	password = models.CharField(max_length = 20)
	age = models.IntegerField()
	gender = models.BooleanField()
	join_date = models.DateTimeField()
	

class Question(models.model)
	user = models.ForeignKey(User)
	id = models.IntegerField()
	text = models.CharField(max_length = 200)
	type = models.CharField(max_length = 20)
	date = models.DateTimeField()