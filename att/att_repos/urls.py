from django.conf.urls import url
from django.contrib import admin
from att_repos import views
urlpatterns = [
    # url(r'^$', views.home),
    url(r'^$', views.AttIssueList.as_view()),
]