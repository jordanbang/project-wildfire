from django.conf.urls import url
from wildfire import views

urlpatterns = [
	url(r'^users/$', views.user_list),
	url(r'^users/(?P<pk>[0-9]+)/$', views.user_detail),
	url(r'^users/update/(?P<pk>[0-9]+)/$', views.user_update),
	url(r'^users/create/$', views.user_create),

	url(r'^question/$', views.question_list),
	url(r'^question/(?P<pk>[0-9]+)/$', views.question_detail),
	url(r'^question/update/(?P<pk>[0-9]+)/$', views.question_update),
	url(r'^question/create/$', views.question_create),
]