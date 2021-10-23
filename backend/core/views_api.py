
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils.date_utils import formatDate, parseStringToDate, parseStringToDateTime

class AsyncSearchView(APIView):
    fields = ...

    def get_queryset(self, term, request):
        ...
    
    def serialize_item(self, item):
        data = {}

        for field in self.fields:
            if hasattr(self, 'get_' + field):
                method = getattr(self, 'get_' + field)
                data[field] = method(item)
            else:
                data[field] = getattr(item, field)
        
        return data
    
    def get(self, request):
        term = request.GET.get('term', '')
        query_set = self.get_queryset(term, request)
        results = [
            {'id': item.pk if hasattr(item, 'pk') else None, **self.serialize_item(item)} 
            for item in query_set
        ]
        return Response(results)

class DataTableView(APIView):
    model = None
    columns_def = []
    hidden_columns = []
    order_by = None

    def user_can_edit(self, user):
        ...

    def get_queryset(self, user):
        ...

    def get_context(self, user):
        return {}

    def filter_by_keyword(self, queryset, keyword):
        return queryset
        
    def get_col(self, col_name):
        col = next((c for c in self.columns_def if c.get('name') == col_name), None)
        if col is not None:
            return col
        
        return next((c for c in self.hidden_columns if c.get('name') == col_name), None)

    def get_model_fields(self, model):
        fields = {}
        for field in model._meta.get_fields():
            fields[field.name] = field
        return fields

    def get_field(self, col):
        if col is None or col.get('name') is None:
            return None

        source = col.get('source', col['name'])
        source_items = source.split('.')
        field = self.model
        n = len(source_items)

        for i,item in enumerate(source_items):
            fields = self.get_model_fields(field) #field._meta.get_fields()
            field = fields.get(item) #next((f for f in fields if f.name == item), None)
            if field is None:
                return None
            if i+1 < n:
                field = field.related_model

        return field

    def getattr_ex(self, obj, attr):
        for item in attr.split('.'):
            if obj is not None:
                obj = getattr(obj, item)
            else:
                return None
        return obj
    
    def serialize_field(self, obj, col_name, context):
        result = {}
        value_id, value = None, None
        col = self.get_col(col_name)
        
        if col is None:
            return {}

        if hasattr(self, f'get_{col_name}'):
            method = getattr(self, f'get_{col_name}')
            value = method(obj, context)
        else:
            field = self.get_field(col)
            field_class = field.__class__.__name__ if field is not None else ''
            source = col.get('source', col.get('name')) 
            value = self.getattr_ex(obj, source)

            if field_class in ['ImageField', 'FileField'] and value is not None:
                value = context['server_url'] + value.url[1:]
            
            if field_class in ['DateField', 'DateTimeField']:
                value = formatDate(value, fmt=col.get('format', '%d/%m/%Y'))
            
            elif field_class == 'ForeignKey':
                value_id = value.pk if value is not None else None
                value = self.getattr_ex(value, col.get('display_field')) if value is not None else ''

            elif field_class == 'ManyToManyField':
                if value is not None:
                    value_id = [str(item.pk) for item in value.all()]
                    value = [self.getattr_ex(item, col.get('display_field')) for item in value.all()]

        if col.get('display_list'):
            value_id = value
            value = next((x for x in col.get('display_list') if x[0] == value), ('', ''))[1]
            
        if isinstance(value, str):
            value = value.replace('\r\n', '<br>').replace('\n', '<br>')

        if value is not None:
            result[col_name] = value

        if value_id is not None:
            result[f'{col_name}_id'] = value_id
        
        return result

    def serialize_object(self, obj, context):
        col_names = [col.get('name') for col in self.columns_def + self.hidden_columns
                        if col.get('name') is not None]
        result = {}
        
        for col_name  in col_names:
            result.update(self.serialize_field(obj, col_name, context))

        result['pk'] = obj.pk
        return result

    def serialize_list(self, lst, context):
        return [self.serialize_object(obj, context) for obj in lst]

    def post(self, request):
        pk = request.data.get('pk')
        col_name = request.data.get('colName')
        value = request.data.get('value', '')
        col = next((c for c in self.columns_def if c.get('name') == col_name) )
        
        if pk and col:
            field = self.get_field(col)
            field_class = field.__class__.__name__

            queryset = self.get_queryset(request.user)
            if queryset is None:
                raise Exception('Method get_queryset not implemented!')

            obj = queryset.get(pk=pk)

            if hasattr(self, f'update_{col_name}'):
                method = getattr(self, f'update_{col_name}')
                method(obj, value)
                return Response({'success': True})
            else:
                source = col.get('source', col_name)
                source_items = source.split('.')
                
                for item in source_items[:-1]:
                    obj = getattr(obj, item)

                if field_class == 'BooleanField':
                    value = value == '1'

                elif field_class in ['IntegerField', 'FloatField']:
                    value = value or None

                elif field_class == 'DateField':
                    value = parseStringToDate(value)

                elif field_class == 'DateTimeField':
                    value = parseStringToDateTime(value)

                elif field_class == 'ForeignKey':
                    value = field.related_model.objects.get(pk=value) if value else None

                if field_class == 'ManyToManyField':
                    db_field = getattr(obj, source_items[-1])
                    db_field.set([x for x in value.split(',') if x != ''])
                else:
                    setattr(obj, source_items[-1], value)
                    
                obj.save()
                return Response({'success': True})
        
        return Response(status=404)

    def get(self, request):
        if request.GET.get('__meta__'):
            columns = []
            for col in self.columns_def:
                field = self.get_field(col)
                field_class = field.__class__.__name__ if field else ''
                
                dtype = {
                    'BooleanField': 'bool',
                    'DateField': 'date',
                    'DateTimeField': 'datetime',
                    'CharField': 'text',
                    'IntegerField': 'number',
                    'FloatField': 'number',
                    'ForeignKey': 'category',
                    'ManyToManyField': 'multiCategory'
                }.get(field_class, 'text')

                display_list = []
                edit_list = []
                search_options = col.get('search_options', {})
                async_search = search_options.get('async', False)
                company_field = search_options.get('company_field', 'company').replace('.', '__')
                status_field = search_options.get('status_field', 'status').replace('.', '__')
                statuses = search_options.get('statuses', ['ACTIVE'])
                extra_filters = search_options.get('extra_filters')

                if col.get('display_list'):
                    dtype = 'category'
                    display_list = col.get('display_list')

                elif field_class in ['ForeignKey', 'ManyToManyField']:
                    display_field = col.get('display_field')
                    if not display_field:
                        raise Exception(f'Foreign field "{col["name"]}" has no display field')

                    related_model_fields = self.get_model_fields(field.related_model)
                    if company_field == 'company' and 'company' not in related_model_fields:
                        raise Exception('No company_field in search_options for column:' + col["name"])

                    if status_field == 'status' and 'status' not in related_model_fields:
                        status_field = None #raise Exception('No status_field in search_options for column:' + col["name"])

                    if not async_search:
                        items = field.related_model.objects.filter(**{company_field: request.user.employee.company})
            
                        if status_field:
                            items = items.filter(**{status_field + '__in': statuses})
                            
                        if extra_filters:
                            items = items.filter(**extra_filters)

                        display_list = [(item.pk, self.getattr_ex(item, display_field)) 
                                            for item in items]

                edit_list = col.get('edit_list', display_list)

                columns.append({
                    'data': col.get('name'),
                    'dtype': dtype,
                    'blank': field.blank if field else False,
                    'asyncSearch': async_search,
                    'title': col.get('title', col.get('name')),
                    'orderable': col.get('orderable', 'name' in col) ,
                    'cssClass': col.get('css_class'),
                    'search': col.get('search', True),
                    'displayList': display_list,
                    'editList': edit_list,
                    'editable': col.get('editable', False) and self.user_can_edit(request.user),
                    'editWidget': col.get('edit_widget', 'input'),
                    'isNarrow': col.get('is_narrow'),
                    'width': f'{col["width"]}' if 'width' in col else None,
                })
           
            return Response(columns)

        if request.GET.get('search_col'):
            term = request.GET.get('term', '').strip()
            col_name = request.GET['search_col']
            col = self.get_col(col_name)
            field = self.get_field(col)
            display_field = col.get('display_field') if col else None
            
            if field is None or display_field is None:
                return Response({'results': []})
            
            search_options = col.get('search_options', {})
            company_field = search_options.get('company_field', 'company').replace('.', '__')
            status_field = search_options.get('status_field', 'status').replace('.', '__')
            statuses = search_options.get('statuses', ['ACTIVE'])
            extra_filters = search_options.get('extra_filters')

            search_key = (display_field + '.icontains').replace('.', '__')
            items = field.related_model.objects.filter(**{company_field: request.user.employee.company,
                                 search_key: term})
            
            if status_field:
                items = items.filter(**{status_field + '__in': statuses})

            if extra_filters:
                items = items.filter(**extra_filters)

            items = items[:30]
            results = [{'id': item.pk, 'display': self.getattr_ex(item, display_field)}
                            for item in items]
            
            return Response({'results': results})

        keyword = request.query_params.get('search', '') 
        start = int(request.query_params.get('start', 0))
        length = int(request.query_params.get('length', 0))
        queryset = self.get_queryset(request.user)
        items = self.filter_by_keyword(queryset, keyword)

        if queryset is None:
            raise Exception('Method get_queryset not implemented!')

        for col in self.columns_def:
            if 'name' not in col:
                continue

            col_name = col['name']
            value = request.GET.get(f'columns[{col_name}][search]', '').strip()

            if value:
                if hasattr(self, f'filter_by_{col_name}'):
                    method = getattr(self, f'filter_by_{col_name}')
                    items = method(items, value)
                else:
                    field = self.get_field(col)
                    if not field:
                        continue

                    filter_rules = []
                    source = col.get('source', col_name)

                    field_class = field.__class__.__name__

                    if field_class in ['DateField', 'DateTimeField']:
                        if value.count('--') == 1:
                            from_date, to_date = value.split('--')
                            from_date, to_date = map(parseStringToDate, [from_date, to_date])
                            to_date = to_date + timedelta(days=1) if to_date else None
                        else:
                            date = parseStringToDate(value)
                            from_date = date
                            to_date = date + timedelta(days=1) if date else None
                        
                        if from_date:
                            filter_rules.append({
                                'source': source, 
                                'filter_cond': 'gte', 
                                'value': from_date
                            })

                        if to_date:
                            filter_rules.append({
                                'source': source, 
                                'filter_cond': 'lt', 
                                'value': to_date
                            })
                    else:
                        filter_cond = ''

                        if field_class in ['CharField', 'EmailField']:
                            filter_cond = 'icontains'

                        if field_class in ['ForeignKey', 'ManyToManyField'] or col.get('display_list'):
                            filter_cond = 'in'
                            value = value.split(',')
                        
                        filter_rules = [
                            {
                                'source': source,
                                'filter_cond': filter_cond,
                                'value': value
                            }
                        ]

                    for rule in filter_rules:
                        source = rule['source'].replace('.', '__')
                        filter_cond = rule['filter_cond']
                        if filter_cond:
                            source += f'__{filter_cond}'
                        
                        items = items.filter(**{source: rule['value']})
                
        order_by = request.GET.get('order_by')
        order_dir = request.GET.get('order_dir', 'asc')

        if order_by:
            order_column = self.get_col(order_by)
            if order_column:
                order_by = order_column.get('source', order_by)
                if order_column.get('display_field'):
                    order_by += '.' + order_column.get('display_field')

                order_by = order_by.replace('.', '__')

                if order_by and order_dir == 'desc':
                    order_by = '-' + order_by
            else:
                order_by = ''
        
        order_by = order_by or (self.order_by or '').replace('.', '__')
                
        items = items.distinct()
        
        if order_by:
            items = items.order_by(order_by)

        total = items.count()
        context = self.get_context(request.user)
        context['server_url'] = request.build_absolute_uri('/')
        data = self.serialize_list(items[start:start+length], context)

        return Response({
            'total': total,
            'data': data
        })