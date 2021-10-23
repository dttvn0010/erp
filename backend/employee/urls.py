from django.urls import path, include
from .views import *

urlpatterns = [
    path('user', list_user),
    path('group', list_group),
    #path('department', list_department),
    path('team', list_team),

    path('department/', include('employee.components.department.urls')),
    path('', include('employee.components.employee.urls')),
]