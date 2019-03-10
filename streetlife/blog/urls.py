from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.Home),
	url(r'^create/$', views.Create),
	url(r'^create/spot/$', views.Create_Spot),
	url(r'^create/street/$', views.Create_Street),
	url(r'^overview/$', views.Overview),	
	url(r'^spot/$', views.Spot, name='spot'),
	url(r'^(?P<pk>\d+)/$', views.Spot_detail, name='spot_detail'),
	url(r'^street/$', views.Street, name='street'),
	url(r'^street/(?P<pk>\d+)$', views.Street_detail, name='street_detail'),
	url(r'^show/spot/(?P<pk>\d+)/$', views.Popup_spot, name='Popup_spot'),
	url(r'^edit/spot/delete/(?P<pk>\d+)/$', views.Delete_Spot, name='delete_spot'),
	url(r'^edit/street/delete/(?P<pk>\d+)/$', views.Delete_Street, name='delete_street'),
	url(r'^edit/spot/(?P<pk>\d+)/$', views.Edit_Spot, name='edit_spot'),
	url(r'^edit/street/(?P<pk>\d+)/$', views.Edit_Street, name='edit_street'),
	url(r'^street/(?P<pk>\d+)/recommend/$', views.Recommend, name='recommend'),
]
