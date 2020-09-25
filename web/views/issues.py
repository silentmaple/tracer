from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

def issues(request,project_id):
    return render(request,'issues.html')
















