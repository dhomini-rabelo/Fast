from django.test import TestCase, Client
from django.test.utils import override_settings
from django.urls import reverse
from datetime import date
from apps.core.models import Person
from django.contrib.auth import get_user_model
from django.core import mail


class BaseForViews(TestCase):
    # main attributes: is_base_class, path
    path: str # request.path, use django.urls.reverse
    is_base_class = True # change to false in children classes
    login_is_required = False
    use_create_users = False

    @classmethod
    def setUpTestData(cls):
        if cls.is_base_class is True: return
        if cls.use_create_users:
            cls.create_users(cls)
        cls.create_models(cls)
        cls.initial_function(cls)
        cls.path = cls.get_path(cls)
        cls.client = Client()
        if cls.login_is_required:
            cls.client = cls.login(cls, cls.client)
        cls.request = cls.client.get(cls.path)

    def get_path(self):
        return self.path

    def initial_function(self): pass

    def _pre_setup(self):
        """
        Perform pre-test setup:
        * Create a test client.
        * Clear the mail test outbox.
        """
        current_client = self.client_class() if not hasattr(self, 'client') else self.client
        super()._pre_setup()
        self.client = current_client

    def create_models(self): pass

    def test_status_code_without_login(self):
        if self.is_base_class is True: return
        client = Client()
        request = client.get(self.path)
        if self.login_is_required:
            self.assertEqual(request.status_code, 302) # redirect for login url
        else:
            self.assertEqual(request.status_code, 200)

    def test_status_code_with_login(self):
        if self.is_base_class is True: return
        self.assertEqual(self.request.status_code, 200)

    def create_users(self):
        UserModel = get_user_model()
        self.users = [
            UserModel.objects.create_user(
                username = f'user {i}',
                email = f'user{i}@mail.com',
                password = f'123456{i}',
        ) for i in range(1, 3 + 1) ]

    def login(self, client: Client):
        UserModel = get_user_model()
        username, password = 'user', '123456'
        user = UserModel(
            username = username,
            email = f'user@mail.com',
            is_staff=True,
        )
        user.set_password(password)
        user.save()
        client.login(username=username, password=password)
        return client

    def make_test_context(self, context_obj: dict, custom_request=None):
        request = self.request.context if custom_request is None else custom_request
        self.assertEqual(context_obj, { k: request[k] for k in context_obj.keys() })

    def assert_404(self, request):
        self.assertIn('<h2 class="text-uppercase text-center">Página não encontrada !</h2>', request.content.decode('utf-8'))

