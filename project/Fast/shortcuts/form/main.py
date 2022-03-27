from .support import construct_form, save_base_form, load_form, save_form_values_and_form_errors, delete_form


def get_form(request, form_nickname: str, form_data: dict):
    
    form_name = f'{form_nickname}_form'
    
    if request.session.get(form_name) is None:
        form = construct_form(form_name, **form_data)
        save_base_form(request, form, form_nickname)
    else:
        form = load_form(request, form_nickname)

    return form.get_form()


def save_form(request, form_nickname: str, fields_values: dict, errors: dict):
    save_form_values_and_form_errors(request, form_nickname, fields_values, errors)
    
    
def delete_used_form(request, form_nickname: str):
    delete_form(request, form_nickname)
    