import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from monitor.client import CeleryClient


class WorkersView(View):

    @staticmethod
    def get(self, request):
        instance = CeleryClient()
        response = instance.workers()
        if not response:
            return HttpResponse(json.dumps([]),content_type="application/json")
        else:
            return HttpResponse(json.dumps(response),content_type="application/json")

    def post(self, request):
        pass


class TasksView(LoginRequiredMixin, View):

    @staticmethod
    def get(self, request):
        instance = CeleryClient()
        response = instance.registered_tasks()
        if not response:
            return HttpResponse(json.dumps([]), content_type="application/json")
        else:
            return HttpResponse(json.dumps(response), content_type="application/json")

    def post(self, request):
        pass


class WorkersIndexView(View):

    @staticmethod
    def get(self, request):
        import time

        a = time.time()
        instance = CeleryClient()
        b = time.time()
        workers = instance.workers()
        c = time.time()
        #print b - a
        #print c - b
        #print c - a
        #print response
        # from django.utils import translation
        # user_language = 'zh-hans'
        ###user_language = 'en'
        # translation.activate(user_language)
        # request.session[translation.LANGUAGE_SESSION_KEY] = user_language
        return render(request, 'monitor/workers.html', {'workers': workers})
