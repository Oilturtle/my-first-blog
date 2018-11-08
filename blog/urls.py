from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^week.html', views.week),
    url(r'^month.html', views.month),
]
