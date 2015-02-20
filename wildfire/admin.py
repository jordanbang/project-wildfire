from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from wildfire.models import UserProfile, Question, Category, Answer
# Register your models here.

class UserProfileInline(admin.StackedInline):
	model = UserProfile
	can_delete = False
	verbose_name_plural = 'User Profiles'


class UserAdmin(UserAdmin):
	inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Question)
admin.site.register(Category)
admin.site.register(Answer)