from layout import MODULES

def layout_pages(request):
    url = request.path_info or ''

    if url.endswith('/'):
        url = url[:-1]
    
    if url.startswith('/'):
        url = url[1:]

    if '/' in url:
        pos = url.rfind('/')
        parent_url = url[:pos]
    else:
        parent_url = ''

    return {'modules': MODULES, 'url': url, 'parent_url': parent_url, 'module_name': ''}