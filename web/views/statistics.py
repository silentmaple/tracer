from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

def statistics(request,project_id):
    return render(request,'statistics.html')
















