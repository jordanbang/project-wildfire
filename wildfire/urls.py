from django.conf.urls import url
from wildfire import views

urlpatterns = [
	url(r'^users/$', views.user_list),
	url(r'^users/(?P<pk>[0-9]+)/$', views.user_detail),
	url(r'^question/$', views.question_list),
	url(r'^question/(?P<pk>[0-9]+)/$', views.question_detail)
]