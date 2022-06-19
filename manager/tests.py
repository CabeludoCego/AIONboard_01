from django.test import TestCase
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest

from .models import Cart

# Create your tests here.
# def testx():
#   assert 2 == 3
def dummy_get_response(request):
    return None

def http_request():
  request = HttpRequest()
  middleware = SessionMiddleware(dummy_get_response)

def session(http_request):
    return http_request.session

def cart(http_request, session):
    cart = Cart(http_request)
    session.modified = False
    return cart