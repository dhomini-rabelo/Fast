from types import FORM_DESCRIPTION

from django.http import HttpRequest
from ...forms.form import Form
from django.core.cache import cache



class UseForm:

    def __init__(self, form_name: str, form_description: FORM_DESCRIPTION, use_history=False, is_dinamic=False):
        self.name = f'{form_name}_form'
        self.fast_name = f'fast_{self.name}_form'
        self.error_name = f'errors_{self.name}_form'
        self.form_description = form_description
        self.use_history = use_history
        self.is_dinamic = is_dinamic
    
    def construct_form(self):
        self.form = Form()
        self.form.add_fields(**self.form_description)
    
    def save_form(self, request: HttpRequest = None, id_: str = None):
        save_name = self.name if not self.is_dinamic else f'{self.name}_{id_}'
        fast_save_name = f'fast_{save_name}'

        if (not self.use_history) and (not self.is_dinamic):
            cache.set(save_name, self.form.form_for_save(), None)
            cache.set(fast_save_name, self.form.fast_load_form(), None)
        else:
            request.session[save_name], = self.form.form_for_save()
            request.session[fast_save_name] = self.form.fast_load_form()
