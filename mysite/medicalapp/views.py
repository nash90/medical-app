from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    homepage_url = settings.STATIC_WEBSITE_URL
    #return HttpResponse("MedScrab is currently under construction…. Please check back later!")
    return HttpResponseRedirect(homepage_url)
