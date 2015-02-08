from django.contrib import admin

from wildfire.models import User, Question, Category, Answer
# Register your models here.
admin.site.register(User)
admin.site.register(Question)
admin.site.register(Category)
admin.site.register(Answer)