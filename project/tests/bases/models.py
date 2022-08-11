from datetime import datetime
from typing import Any, Callable
from django.test import TestCase
from unittest import expectedFailure
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.db.models import Model
from django.db.utils import IntegrityError
from django.db import transaction



class BaseForTestModels(TestCase):
    # main attributes: is_base_class, simple_queryset
    required_fields: list[str] = [] # name of required fields
    unique_fields: list[str] = [] # name of unique fields
    default_values: dict[str, Any] = {} # key -> attr name, value -> default_value
    data_for_default_values_test: dict[str, Any] = {} # data for create obj without fields default_value
    simple_queryset: QuerySet # without .objects.all()
    is_base_class = True # change to false in children classes
    # create_models -> create models for tests or change setUpTestData

    @classmethod
    def setUpTestData(cls):
        if cls.is_base_class is True: return
        cls.create_users(cls)
        cls.create_models(cls)
        cls.queryset = cls.simple_queryset.objects.all()
        cls.obj = cls.queryset.first()

    def create_users(self):
        UserModel = get_user_model()
        self.users = [
            UserModel.objects.create_user(
                username = f'user {i}',
                email = f'user{i}@mail.com',
                password = f'123456{i}',
        ) for i in range(1, 3 + 1) ]

    def create_models(self) -> None:
        # create models here
        raise Exception('NotImplementedMethod')

    #* DEFAULT MODEL TESTS

    def test_required_fields_error(self):
        if self.is_base_class is True or self.required_fields == []: return
        for required_field in self.required_fields:
            try:
                with transaction.atomic():
                    setattr(self.obj, required_field, None)
                    self.obj.save()
            except IntegrityError:
                continue
            raise Exception(f'{required_field} is not required')


    def test_unique_fields_error(self):
        if self.is_base_class is True or self.unique_fields == []: return
        for unique_field in self.unique_fields:
            try:
                with transaction.atomic():
                    setattr(self.obj, unique_field, getattr(self.queryset.last(), unique_field))
                    self.obj.save()
            except IntegrityError:
                continue
            raise Exception(f'{unique_field} is not unique')

    def test_default_values(self):
        if self.is_base_class is True or self.default_values == {}: return
        new_obj = self.queryset.create(**self.data_for_default_values_test)
        for attr_name, attr_value in self.default_values.items():
            new_obj_attr_value = getattr(new_obj, attr_name)
            self.assertEqual(new_obj_attr_value, attr_value)
