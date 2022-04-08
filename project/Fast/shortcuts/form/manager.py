from types import FORM_DESCRIPTION
from django.http import HttpRequest
from ...forms.form import Form
from django.core.cache import cache



class UseForm:

    def __init__(self, form_name: str, form_description: FORM_DESCRIPTION, is_dinamic=False, many=False, id_: str = None, form_class=Form):
        self.name = f'{form_name}_form' if not many else f'{form_name}_{id_}_name'
        self.fast_name = f'fast_{self.name}'
        self.errors_name = f'errors_{self.name}'
        self.fields_name = f'fields_{self.name}'
        self.form_description = form_description
        self.is_dinamic = is_dinamic
        self.many = many
        self.is_basic = (not is_dinamic) and (not many)
        self.is_complex = is_dinamic and many

    def adapt_dinamic_data(self, adapt_function: function):
        adapt_function(self.form_description)
    
    def construct_form(self):
        self.form = self.form_class()
        self.form.add_fields(**self.form_description)
    
    def save_used_form(self, request: HttpRequest = None, fields: dict[str, str]={}, errors: dict[str, str]={}):
        request.session[self.fields_name] = fields.copy()
        request.session[self.errors_name] = errors.copy()

    def delete_used_form(self, request: HttpRequest = None):
        request.session[self.fields_name] = None
        request.session[self.errors_name] = None
    
    def save_form_base(self, request: HttpRequest = None):
        if self.is_basic:
            cache.set(self.name, self.form.form_for_save(), None)
            cache.set(self.fast_name, self.form.fast_load_form(), None)
        else:
            request.session[self.name], = self.form.form_for_save()
            request.session[self.fast_name] = self.form.fast_load_form()

    def delete_form_base(self, request: HttpRequest = None):
        if self.is_basic:
            cache.set(self.name, None, None)
            cache.set(self.fast_name, None, None)
        else:
            request.session[self.name] = None
            request.session[self.fast_name] = None

