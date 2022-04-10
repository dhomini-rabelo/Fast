from ....forms.form import Form
from .support import get_form_settings, construct_form, save_base_form, save_form_values_and_form_errors, load_form_and_delete_used_form



def get_form(request, form_nickname: str, id_: str, form_data: dict, form_class=Form):

    form_settings = get_form_settings(request, f'{form_nickname}_{id_}', form_class)

    if request.session.get(form_settings['name']) is None:
        form = construct_form(form_settings, **form_data)
        save_base_form(request, form_settings, form)
        return form.get_form()

    return load_form_and_delete_used_form(request, form_settings)


def save_form(request, form_nickname: str, fields_values: dict, errors: dict, form_class=Form):
    form_settings = get_form_settings(request, form_nickname, form_class)
    save_form_values_and_form_errors(request, form_settings, fields_values, errors)


def delete_used_form(request, form_nickname: str, form_class=Form):
    form_settings = get_form_settings(request, form_nickname, form_class)
    request.session[form_settings['used_form']] = None
    
