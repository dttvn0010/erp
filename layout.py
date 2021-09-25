
PERMISSION_ALL = lambda u : True
PERMISSION_STAFF = lambda u : u.is_staff

def has_permission(permission_name):
    short_name = permission_name.split('.')[-1]
    if short_name.count('_') == 1:
        action, object = short_name.split('_')
        if action == 'view':
            permission_names = [ 
                permission_name,
                f'add_{object}',
                f'change_{object}',
                f'delete_{object}',
            ]
            return has_any_permissions(permission_names)

    return lambda u : u.has_perm(permission_name)

def has_any_permissions(permission_names):
    return lambda u : any(u.has_perm(permission_name) for permission_name in permission_names)

def has_all_permissions(permission_names):
    return lambda u : all(u.has_perm(permission_name) for permission_name in permission_names)

class Page:
    def __init__(self, route, title='', icon='', url='', children=None, permission_checker=None):
        self.parent = None
        self.route = route
        self.title = title
        self.icon = icon
        self._url = url
        self.children = children
        
        if self.children:
            for child in self.children:
                child.parent = self

        self.permission_checker = permission_checker

    @property
    def url(self):
        if self._url:
            return self._url

        elif self.parent is None or self.parent.url == '':
            return  self.route

        else:
            return self.parent.url + '/' + self.route

    @property
    def url_prefix(self):
        if self.module and self.module.name:
            return self.module.name + '/'
        else:
            return ''

class Module:
    def __init__(self, title, name, pages):
        self.title = title
        self.name = name
        self.pages = pages
        for page in pages:
            page.module = self

    def __str__(self):
        return self.name

MODULES = [
    Module('ERP Core', '', [
        Page('employee', 'Quản lý nhân viên', url='employee', children=[
            Page('user', 'Tài khoản người dùng', permission_checker=has_permission('auth.view_user')),
            Page('group', 'Vai trò', permission_checker=has_permission('auth.view_group')),
            Page('department', 'Phòng ban', permission_checker=has_permission('core.view_department')),
            Page('team', 'Nhóm làm việc', permission_checker=has_permission('core.view_team')),
        ]),
    ])
]

def get_module_by_name(module_name):
    return next((m for m in MODULES if m.name == module_name), None)

def find_page_by_url(pages, url):
    for page in pages:
        if page.url == url:
            return page
            
        if page.children:
            child_page = find_page_by_url(page.children, url)
            if child_page:
                return child_page

def get_page_by_url(module, url):
    if module:
        return find_page_by_url(module.pages, url)

if __name__ == '__main__':
    m = get_module_by_name('react-app')
    p = get_page_by_url(m, 'about')
    print(p.url)