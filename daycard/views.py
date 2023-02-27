from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	context_dict = {}
	return render(request, 'daycard/index.html', context=context_dict)