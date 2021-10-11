from django.template.defaulttags import register
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from layout import get_module_by_name, get_page_by_url, has_permission_func

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
def startswith_url(st1, st2):
    if isinstance(st1, str) and isinstance(st2, str):
        if not st1.endswith('/'):
            st1 += '/'
        
        if not st2.endswith('/'):
            st2 += '/'

        return st1.startswith(st2)
    
    return False

@register.filter
def has_page_permission(user, page):
    return not page.permission_checker or user.is_admin or page.permission_checker(user)

@register.filter
def has_module_permission(user, module):
    for page in module.pages:
        if not page.children and has_page_permission(user, page):
            return True

        if page.children and has_any_page_permission(user, page.children):
            return True
    
    return False

@register.filter
def has_any_page_permission(user, pages):
    return any(has_page_permission(user, page) for page in pages)

@register.filter
def has_permission(user, permission_name):
    func = has_permission_func(permission_name)
    return func(user)

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def app(request):
    return render(request, 'app.html')