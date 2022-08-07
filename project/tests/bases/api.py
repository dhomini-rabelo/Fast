from tests.bases.views import BaseForViews



class BaseForApi(BaseForViews):
    main_method = 'POST'
    fk_fields: dict[str, (str('int') | str("uuid")) ] = {}
    required_fields: list[str] = []
    time_fields: list[str] = []
    choice_fields: list[str] = []
    date_fields: list[str] = []

    def test_required_fields(self):
        if self.is_base_class is True: return
        data = { k:v for k,v in self.valid_data.items() if k not in self.required_fields }
        request = self.do_request(data)
        for field in self.required_fields:
            self.assertEqual(str(request.data[field][0]), 'Este campo é obrigatório.')

    def test_fk_fields(self):
        if self.is_base_class is True: return
        invalid_ids = {'int': 0, 'uuid': '6b340c0d-9200-46b0-b93e-a9999a999999'}
        data = self.valid_data.copy()
        for field_name, id_type in self.fk_fields.items():
            data[field_name] = invalid_ids[id_type]
        request = self.do_request(data)
        for field_name, id_type in self.fk_fields.items():
            self.assertEqual(str(request.data[field_name][0]), f'Pk inválido "{invalid_ids[id_type]}" - objeto não existe.')

    def test_time_fields(self):
        if self.is_base_class is True: return
        data = self.valid_data.copy()
        for field in self.time_fields:
            data[field] = '17/05/2005'
        request = self.do_request(data)
        for field in self.time_fields:
            self.assertEqual(str(request.data[field][0]), 'Formato inválido para Tempo. Use um dos formatos a seguir: hh:mm[:ss[.uuuuuu]].')

    def test_date_fields(self):
        if self.is_base_class is True: return
        data = self.valid_data.copy()
        for field in self.date_fields:
            data[field] = '17/03/2003'
        request = self.do_request(data)
        for field in self.date_fields:
            self.assertEqual(str(request.data[field][0]), 'Formato inválido para data. Use um dos formatos a seguir: YYYY-MM-DD.')

    def test_choice_fields(self):
        if self.is_base_class is True: return
        data = self.valid_data.copy()
        for field in self.choice_fields:
            data[field] = 'invalid_option_for_choice'
        request = self.do_request(data)
        for field in self.choice_fields:
            self.assertEqual(str(request.data[field][0]), '"invalid_option_for_choice" não é um escolha válido.')

    def do_request(self, data: dict):
        if self.main_method == 'POST':
            request = self.client.post(self.path, data=data, content_type='application/json')
        elif self.main_method == 'PUT':
            request = self.client.put(self.path, data=data, content_type='application/json')
        else:
            raise Exception('Invalid: self.main_method')
        return request



class BaseForUpdateApi(BaseForViews):

    def test_status_code_without_login(self): pass

    def test_status_code_with_login(self): pass