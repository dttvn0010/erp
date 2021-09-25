from django.template.defaulttags import register
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from layout import get_module_by_name, get_page_by_url

@register.inclusion_tag('tags/async_select.html')
def async_select(id, initial=None, display_field='name', pk_field='pk', multiple=False):
    if multiple:
        options = initial or []
    else:
        options = [initial] if initial else []
    
    options = [{
        'value': getattr(option, pk_field), 
        'display' : getattr(option, display_field) 
    } for option in options] 

    return {
        'id': id,
        'options': options,
        'multiple': multiple
    }

@register.filter
def has_page_permission(user, page):
    return not page.permission_checker  or page.permission_checker(user)

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def app(request):
    return render(request, 'app.html')