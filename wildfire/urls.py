from django.conf.urls import url, include
from wildfire import views

urlpatterns = [
	url(r'^users/$', views.user_list),
	url(r'^users/(?P<pk>[0-9]+)/$', views.user_detail),
	url(r'^users/update/(?P<pk>[0-9]+)/$', views.user_detail),
	url(r'^users/create/$', views.user_create),

	url(r'^question/$', views.question_list),
	url(r'^question/(?P<pk>[0-9]+)/$', views.question_detail),
	url(r'^question/update/(?P<pk>[0-9]+)/$', views.question_update),
	url(r'^question/create/$', views.question_create),
	
	url(r'^answers/$', views.answer_list),
	url(r'^answers/(?P<pk>[0-9]+)/$', views.answer_detail),
	url(r'^answers/update/(?P<pk>[0-9]+)/$', views.answer_update),
	url(r'^answers/create/$', views.answer_create),

	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^login/$', views.GetAuthToken.as_view(), name='authenticate'),
	url(r'^logout/$', views.wild_logout),
	
	url(r'^stats/(?P<pk>[0-9]+)/$', views.stats),

	url(r'^profile/(?P<pk>[0-9]+)/$', views.profile),
	url(r'^connect/$', views.connect),
	url(r'^search/$', views.search),
	url(r'^replies/(?P<pk>[0-9]+)/$', views.replies),
]