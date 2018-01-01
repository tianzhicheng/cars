# _*_codding:utf-8_*_
from django.http import HttpRequest, HttpResponse

from django.shortcuts import render
from django.views.generic.base import View
from utils.Constant import AJAX_HEADER


class LoginView(View):
    def get(self, request):
        # type: (object) -> object
        pass

    def post(self, request):
        pass


class TestView(View):
    def get(self, request):
        # type: (object) -> object
        return HttpResponse(content='{"msg":"success"}', content_type=AJAX_HEADER)

    def post(self, request):
        return HttpResponse(content='{"msg":"success"}', content_type=AJAX_HEADER)
