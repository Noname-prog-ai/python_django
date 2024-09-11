from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def set_cookie(request):
    response = HttpResponse("Cookie Set")
    response.set_cookie('my_cookie', 'cookie_value')
    return response


def get_cookie(request):
    value = request.COOKIES.get('my_cookie', 'default_value')
    return HttpResponse(f"Cookie Value: {value}")


def set_session(request):
    request.session['my_session'] = 'session_value'
    return HttpResponse("Session Set")


def get_session(request):
    value = request.session.get('my_session', 'default_value')
    return HttpResponse(f"Session Value: {value}")
