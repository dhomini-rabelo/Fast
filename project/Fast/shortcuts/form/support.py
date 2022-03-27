from Support.Code.actions.Support.forms.form import Form
from .loaded import loaded_forms
from Support.Code.actions.Support.utils.main import gets

    

base_changes = [('[name]', 'name'), ('[label]', 'label'), ('[placeholder]', 'placeholder')]
def construct_form(form_name: str, fields: list[dict], html_structure: str, changes=base_changes) -> Form:
    page_form = Form()

    if form_name in loaded_forms.keys() and f'fast_{form_name}' in loaded_forms.keys():
        page_form.fast_load_form(loaded_forms[form_name], loaded_forms[f'fast_{form_name}'])
    else:
        page_form.add_fields(fields, html_structure, changes)
        
    return page_form


def delete_form(request, form_nickname: str):
    request.session[f'{form_nickname}_form_errors'] = None
    request.session[f'{form_nickname}_fields'] = None



def load_form(request, form_nickname: str) -> Form:
    page_form = Form()
    
    form_name = f'{form_nickname}_form'
    form_fields = f'{form_nickname}_fields'
    form_errors = f'{form_nickname}_form_errors'

    
    if request.session.get(form_fields) is None:
        page_form.fast_load_form(request.session[form_name], request.session[f'fast_{form_name}'])
    else:
        if request.session.get(form_errors) is None:
            page_form.load_form_with_values(request.session[form_name], request.session[form_fields])
        else:
            page_form.load_form_with_values(request.session[form_errors], request.session[form_fields])

    delete_form(request, form_nickname)
    
    return page_form



def save_base_form(request, form_class: Form, form_nickname: str):
    request.session[f'{form_nickname}_form'] = form_class.form_for_save()
    request.session[f'fast_{form_nickname}_form'] = form_class.form


def save_form_values_and_form_errors(request, form_nickname: str, fields_values: dict, errors: dict):
    
    form_name = f'{form_nickname}_form'
    form_fields = f'{form_nickname}_fields'
    form_errors = f'{form_nickname}_form_errors'
    

    if fields_values != {}:
        request.session[form_fields] = fields_values
    else:
        request.session[form_fields] = None

    if errors != {}:
        page_form = Form()
        page_form.load_form(request.session[form_name])
        page_form.show_errors(errors)
        request.session[form_errors] = page_form.form_for_save()
    else:
        request.session[form_errors] = None
