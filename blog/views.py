from django.http import HttpResponse
from requests import get, post
import json

def home(req, text):
    return HttpResponse('Hell0 {}!'.format(text))
 



