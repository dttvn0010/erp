from django.shortcuts import render

def list_location(request):
    return render(request, 'location/list.html')