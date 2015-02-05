from django.contrib import admin

from wildfire.models import User, Question, Categories, MultipleChoiceOptions, RangeOptions, Answers
# Register your models here.
admin.site.register(User)
admin.site.register(Question)
admin.site.register(Categories)
admin.site.register(MultipleChoiceOptions)
admin.site.register(RangeOptions)
admin.site.register(Answers)