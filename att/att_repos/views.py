from django.shortcuts import render
import requests
# Create your views here.
from django.http import (HttpResponse,
                         HttpResponseRedirect,
                         JsonResponse)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from restkit import Resource, BasicAuth, Connection, request
from requests.auth import HTTPBasicAuth
from socketpool import ConnectionPool
from django.contrib.auth.decorators import login_required
import urllib2
from decouple import config
__author__ = "Santosh Kesireddy"
__email__ = "santosh981k@gmail.com"
class LoginRequiredMixin(object):
    def __init__(self):
        self.doc_string = \
        "Login required class for class based views"
    @classmethod
    def as_view(cls):
        return login_required(
        	super(LoginRequiredMixin, cls).as_view())
    def __doc__(self):
    	return self.doc_string
@login_required
def home(request):
	return JsonResponse("OAUTH2 worked",safe=False)
class AttIssueList(APIView):
    def __init__(self):
        self.doc_string = " Att Public Repo open isues API"
        self.CLIENT_ID = config('CLIENT_ID')
        self.CLIENT_SECRET = config('CLIENT_SECRET')
    def authentication(self):
    	#Future implementation 
		pass
    def get_modified_list(self,obj):
    	#returns updated open issues list with comments if exists
    	#Parameters: Obj- list all att open issues from public repos
        for each_obj in obj:
            if each_obj['comments']:
                rate_limit = '?client_id='+self.CLIENT_ID+'&client_secret='+self.CLIENT_SECRET
                each_obj["comments_data"] = \
                json.loads(requests.get(each_obj["comments_url"]+rate_limit).text)
        return obj

    def get(self,request):
        """
           Returns list of all open issues for all public repositories owned 
           by the "att" organization. Each issue object also contain a 
           list of comments if any exists
        """

        try:
        	#request to get att public repositories
        	att_repos_obj = requests.get(
        	"https://api.github.com/orgs/att/repos?client_id="+self.CLIENT_ID+"&client_secret="+self.CLIENT_SECRET)
        except TypeError:
        	return JsonResponse("Rate Limit Exceded.")
        #Att Repos Data extraction from response object att_repos_obj 
        att_repos_dict_objs = json.loads(att_repos_obj.text)
        repo_names = [reponame['name'] for reponame in att_repos_dict_objs]
        att_open_issues_list=[]
        for repo_name in repo_names:
            url = "https://api.github.com/repos/att/"+repo_name+"/issues?state=open&client_id="+self.CLIENT_ID+"&client_secret="+self.CLIENT_SECRET
            att_repo_response = requests.get(url)
            att_repo_list_of_dict_objs = json.loads(att_repo_response.text)
            att_open_issues_list.extend(att_repo_list_of_dict_objs)
        att_open_issues_list = self.get_modified_list(att_open_issues_list)
        # return JsonResponse(att_open_issues_list,safe=False)
        return Response(att_open_issues_list)
    def __doc__(self):
    	return self.doc_string
    
