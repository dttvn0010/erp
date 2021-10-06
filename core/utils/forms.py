from django import forms
from django.forms import utils

from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape, format_html, format_html_join
from django.utils.translation import gettext_lazy as _

class ErrorList(utils.ErrorList):
    def __init__(self, initlist=None, error_class=None, field_name=None):
        super().__init__(initlist, error_class)
        self.field_name = field_name

    def as_ul(self):
        if not self.data:
            return ''

        return format_html(
            '<ul id="{}" class="{}" style="color:red">{}</ul>',
            self.field_name + '_errors' if self.field_name else '',
            self.error_class,
            format_html_join('', '<li>{}</li>', ((e,) for e in self))
        )

class AsyncSelect(forms.widgets.ChoiceWidget):
    template_name = 'widgets/select.html'
    option_template_name = 'widgets/select_option.html'
    add_id_index = False

    def options(self, name, value):
        options = []
        queryset = self.queryset
        value = [x for x in value if x.isdigit()]
        print('value=', value)

        if queryset is not None:
            objs = queryset.filter(pk__in=value)
            for index, obj in enumerate(objs):
                options.append(
                    self.create_option(
                        name, obj.pk, str(obj), True, index
                    )
                )
        
        return options

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        return {
            'name': name,
            'value': value,
            'label': label,
            'selected': selected,
            'index': str(index),
            'attrs': {'selected': selected},
            'type': 'select',
            'template_name': self.option_template_name,
            'wrap_label': True,
        }

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['options'] = self.options(name, context['widget']['value'])
        return context

    def use_required_attribute(self, initial):
        return False

class ModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs['error_class'] =  ErrorList
        super().__init__(*args, **kwargs)

    def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        "Output HTML. Used by as_table(), as_ul(), as_p()."
        # Errors that should be displayed above all fields.
        top_errors = self.non_field_errors().copy()
        output, hidden_fields = [], []

        for name, field in self.fields.items():
            html_class_attr = ''
            bf = self[name]
            bf_errors = self.error_class(bf.errors, field_name=name)
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend(
                        [_('(Hidden field %(name)s) %(error)s') % {'name': name, 'error': str(e)}
                         for e in bf_errors])
                hidden_fields.append(str(bf))
            else:
                # Create a 'class="..."' attribute if the row should have any
                # CSS classes applied.
                css_classes = bf.css_classes()
                if css_classes:
                    html_class_attr = ' class="%s"' % css_classes

                if errors_on_separate_row and bf_errors:
                    output.append(error_row % str(bf_errors))

                if bf.label:
                    label = conditional_escape(bf.label)
                    if field.required:
                        label += '*'
                    label = bf.label_tag(label) or ''
                else:
                    label = ''

                if field.help_text:
                    help_text = help_text_html % field.help_text
                else:
                    help_text = ''

                output.append(normal_row % {
                    'errors': bf_errors,
                    'label': label,
                    'field': bf,
                    'help_text': help_text,
                    'html_class_attr': html_class_attr,
                    'css_classes': css_classes,
                    'field_name': bf.html_name,
                })

        if top_errors:
            output.insert(0, error_row % top_errors)

        if hidden_fields:  # Insert any hidden fields in the last row.
            str_hidden = ''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = (normal_row % {
                        'errors': '',
                        'label': '',
                        'field': '',
                        'help_text': '',
                        'html_class_attr': html_class_attr,
                        'css_classes': '',
                        'field_name': '',
                    })
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
        return mark_safe('\n'.join(output))

class AsyncModelChoiceField(forms.ModelChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = AsyncSelect
        
        if 'multiple' in kwargs:
            self.multiple = kwargs.pop('multiple')
        else:
            self.multiple = False

        super().__init__(*args, **kwargs)
        self.widget.queryset = self.queryset

    def widget_attrs(self, widget):
        return {'multiple': self.multiple, 'class': 'async-select'}

    def _set_queryset(self, queryset):
        super()._set_queryset(queryset)
        if self.widget:
            self.widget.queryset = queryset 

    queryset = property(forms.ModelChoiceField._get_queryset, _set_queryset)
