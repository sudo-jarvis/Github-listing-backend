import requests

from core.utils import getRepoLanguages
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from github_listing_backend.settings import GITHUB_API
# Create your views here.
class UserClass(GenericAPIView):
    def get(self, request, format=None):

        response_data = {}
        username = self.request.query_params.get('username', None)
        success = True
        if username is None:
            success = False
            response_data = {"Error": "Username Cannot Be Empty !"}

        request_url = GITHUB_API + 'users/' + username
        req = requests.get(request_url)

        if req.status_code == 404:
            status = (404, "Username Not Found")
            response_data["status"] = status[1]
            return Response(response_data, status[0])

        if not req.ok:
            status = (req.status_code, "Error ! !")
            response_data["status"] = status[1]
            return Response(response_data, status[0])

        req = req.json()
        try:
            name = req['name']
        except Exception as e:
            status = (400, "Free API Limit Exceeded")
            response_data["status"] = status[1]
            return Response(response_data, status[0])

        user = {
            'username': req['login'],
            'name': req['name'],
            'bio': req['bio'],
            'location': req['location'],
            'twitter_url': req['twitter_username'],
            'github_url': 'https://www.github.com/'+req['login'],
            'image_url': req['avatar_url'],
            'repos_url': req['repos_url']
        }

        status = (201, "Success") if success else (400, "Failure")
        response_data['user'] = user
        response_data["status"] = status[1]
        return Response(response_data, status[0])


class RepoClass(GenericAPIView):
    def get(self, request, format=None):

        response_data = {}
        username = self.request.query_params.get('username', None)
        page = self.request.query_params.get('page', None)
        success = True
        if username is None:
            status = (400, "Username Cannot Be Empty !")
            response_data["status"] = status[1]
            return Response(response_data, status[0])

        if page is None:
            status = (400, "Page Number Cannot Be Empty !")
            response_data["status"] = status[1]
            return Response(response_data, status[0])

        request_url = GITHUB_API + 'users/' + username + '/repos?page=' + page
        req = requests.get(request_url)
        if not req.ok:
            status = (req.status_code, "Error ! !")
            response_data["status"] = status[1]
            return Response(response_data, status[0])
        else:
            req = req.json()
        repos = []
        for repo in req:
            repos.append({
                "id": repo['id'],
                "url": repo['html_url'],
                "languages": getRepoLanguages(repo['languages_url']),
                "name": repo['name'],
                "description": repo['description']
            })

        status = (201, "Success") if success else (400, "Failure")
        response_data["status"] = status[1]
        response_data["repos"] = repos
        return Response(response_data, status[0])
