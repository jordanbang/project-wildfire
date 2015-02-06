from django.contrib import admin

from wildfire.models import User, Question, Category, MultipleChoiceOption, RangeOption, Answer
# Register your models here.
admin.site.register(User)
admin.site.register(Question)
admin.site.register(Category)
admin.site.register(MultipleChoiceOption)
admin.site.register(RangeOption)
admin.site.register(Answer)