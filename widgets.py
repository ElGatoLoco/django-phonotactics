from django import forms
from django.template.loader import render_to_string
from django.utils.encoding import force_unicode, force_text
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape, format_html

class IntegerRangeWidget(forms.widgets.Widget):
    template_name = 'integer-range-field.html'

    def render(self, name, value, attrs=None):
        context = {
            'name':name,
            'value':value or self.attrs['default'] or self.attrs['min_value'],
            'minValue':self.attrs['min_value'],
            'maxValue':self.attrs['max_value'],
        }
        return mark_safe(render_to_string(self.template_name, context))

class CustomRadioInput(forms.widgets.RadioChoiceInput):
    def render(self, name=None, value=None, attrs=None, choices=()):
        name = name or self.name
        value = value or self.value
        attrs = attrs or self.attrs
        label_for = ' for="%s"' % (self.attrs['id'])
        choice_label = conditional_escape(force_unicode(self.choice_label))
        return mark_safe(u'<div class="text-center">%s<label %s>%s</label></div>' % (self.tag(), label_for, choice_label))

class RadioCustomRenderer(forms.widgets.RadioFieldRenderer):
    choice_input_class = CustomRadioInput
    outer_html = '<ul class="row" {id_attr}>{content}</ul>'

    def render(self):
        b = unicode(12/len(self.choices))
        class_name = 'col-xs-12 col-md-' + b
        self.inner_html = '<li class="' + class_name + '">{choice_value}{sub_widgets}</li>'
        
        id_ = self.attrs.get('id')
        output = []
        for i, choice in enumerate(self.choices):
            choice_value, choice_label = choice
            if isinstance(choice_label, (tuple, list)):
                attrs_plus = self.attrs.copy()
                if id_:
                    attrs_plus['id'] += '_{}'.format(i)
                sub_ul_renderer = self.__class__(
                    name=self.name,
                    value=self.value,
                    attrs=attrs_plus,
                    choices=choice_label,
                )
                sub_ul_renderer.choice_input_class = self.choice_input_class
                output.append(format_html(
                    self.inner_html, choice_value=choice_value,
                    sub_widgets=sub_ul_renderer.render(),
                ))
            else:
                w = self.choice_input_class(self.name, self.value, self.attrs.copy(), choice, i)
                output.append(format_html(self.inner_html, choice_value=force_text(w), sub_widgets=''))
        return format_html(
            self.outer_html,
            id_attr=format_html(' id="{}"', id_) if id_ else '',
            content=mark_safe('\n'.join(output)),
        )
