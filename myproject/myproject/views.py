#from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
    #the render is used to get the html file on the browser
    return render(request, 'home.html')

def about(request):
    #return HttpResponse("This is the about page.")
    return render(request, 'about.html')