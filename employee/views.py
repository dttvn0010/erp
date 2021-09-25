from django.shortcuts import render

# Create your views here.
def list_user(request):
    return render(request, 'employee/user/list.html')

def list_group(request):
    return render(request, 'employee/group/list.html')

def list_department(request):
    return render(request, 'employee/department/list.html')

def list_team(request):
    return render(request, 'employee/team/list.html')