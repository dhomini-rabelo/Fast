from types import FunctionType
from rest_framework.serializers import ModelSerializer, ValidationError
from django.db.models.query import QuerySet
from django.db.models import Model
from abc import ABC



class ManyChildSerializers:
    """
    This class helps to use children serializers
    """
    simple_get_data = lambda self, field_name : (lambda instance, validated_data : validated_data[field_name])

    def get_data(self, instance: Model, validated_data: dict):
        """
        Get body data for related fields

        Args:
            instance (Model): current model serializer instance
            validated_data (dict): cleaned body data

        require: 
            self.obj_for_get_related_field_data -> dict[str, FunctionType(instance, validated_data) => dict[str, Union[list[dict], dict]]
        """
        related_functions, related_fields_data = self.obj_for_get_related_field_data(), {}
        for related_field in related_functions.keys():
            if related_field not in validated_data.keys(): continue
            get_data: FunctionType = related_functions[related_field]
            related_fields_data[related_field] = get_data(instance, validated_data)
            del validated_data[related_field]
        return related_fields_data, validated_data

    def get_data_with_id(self, field_name):
        return lambda instance, validated_data : [{
            'id': obj_data.get('id'), 
            **obj_data,
        } for obj_data in self.initial_data[field_name]]

    def get_or_error(
        self, queryset: QuerySet, pk_kwargs: dict = {}, error_obj = {}
    ) -> Model: # for foreign key
        relationship_instance = queryset.filter(**pk_kwargs).first()

        if relationship_instance is None:
            raise ValidationError(error_obj)
        return relationship_instance
    
    def get_or_create_instance(
        self, data: dict, serializer_class: ModelSerializer, queryset: QuerySet,
        pk_kwargs: dict = {}, instance_id: int = None, related_name: str = '',
    ) -> Model: # for foreign key
        relationship_instance = queryset.filter(**pk_kwargs).first()

        if relationship_instance is None:
            return self.create_instance(data, serializer_class, instance_id, related_name)
        return relationship_instance

    def update_instance(
        self, instance: Model, data: dict, serializer_class: ModelSerializer,
        instance_id: int = None, related_name: str = ''
    ) -> Model: # for o2o and foreign key
        if instance_id is not None:
            data[related_name] = instance_id
        serializer = serializer_class(instance=instance, data=data)
        if serializer.is_valid():
            relationship_instance = serializer.save()
            return relationship_instance
        raise ValidationError(serializer.errors)        

    def update_current_instance(self, instance, validated_data):
        for attribute_name, value in validated_data.items():
            if value is None: continue
            setattr(instance, attribute_name, value)
        instance.save()
        return instance

    def create_or_update_instance(
        self, data: dict, serializer_class: ModelSerializer, queryset: QuerySet,
        pk_kwargs: dict = {}, instance_id: int = None, related_name: str = '',
    ) -> Model: # for foreign key
        relationship_instance = queryset.filter(**pk_kwargs).first()
        delete_id = lambda key: key if not key.endswith('_id') else key[:-3] # delete _id

        if relationship_instance is None:
            obj_data = {delete_id(k):v for k,v in data.items()}
            return [self.create_instance(obj_data, serializer_class, instance_id, related_name), True]
        return [self.update_instance(relationship_instance, data, serializer_class, instance_id, related_name), False]

    def create_or_update_many(
        self, data: list, serializer_class: ModelSerializer, queryset: QuerySet,
        pk_kwargs: dict = {},  instance_id: int = None, related_name: str = '',
        add_in_related_queryset=False,
    ): # m2m or m2o
        for obj in data:
            adapted_kwargs = {k: obj.get(v)  for k, v in pk_kwargs.items()}
            model, model_was_created = self.create_or_update_instance(obj, serializer_class, queryset, adapted_kwargs, instance_id, related_name)
            if add_in_related_queryset and model_was_created:
                queryset.add(model)

    def create_instance(
        self, data: dict, serializer_class: ModelSerializer,
        instance_id: int = None, related_name: str = ''
    ) -> Model: # for o2o and foreign key
        if instance_id is not None:
            data[related_name] = instance_id
        serializer = serializer_class(data=data)
        if serializer.is_valid():
            relationship_instance = serializer.save()
            return relationship_instance
        raise ValidationError(serializer.errors)

    def create_many(
        self, data: list, serializer_class: ModelSerializer,
        instance_id: int = None, related_name: str = ''
    ): # m2m or m2o
        for obj in data:
            self.create_instance(obj, serializer_class, instance_id, related_name)

    def error_or_update_instance(
        self, data: dict, queryset: QuerySet, serializer_class: ModelSerializer, pk_kwargs: dict = {}, 
        error_obj = {}, instance_id: int = None, related_name: str = '',
    ) -> Model: # for foreign key
        relationship_instance = queryset.filter(**pk_kwargs).first()

        if relationship_instance is None:
            raise ValidationError(error_obj)
        return self.update_instance(relationship_instance, data, serializer_class, instance_id, related_name)
    
    def error_or_update_many(
        self, data: list, queryset: QuerySet, pk_kwargs: dict = {}, error_obj = {}
    ) -> Model: # for foreign key
        for obj in data:
            adapted_kwargs = {k: obj.get(v)  for k, v in pk_kwargs.items()}
            self.error_or_update_instance(obj, queryset, adapted_kwargs, error_obj)

    def _validate_ids_for_delete(self, ids_for_delete: list, related_name: str):
        if not isinstance(ids_for_delete, list):
            raise ValidationError({f'delete_{related_name}': f'delete_{related_name} must be a list'})
        if not all([isinstance(id_, str) for id_ in ids_for_delete]):
            raise ValidationError({f'delete_{related_name}': f'delete_{related_name} contains invalid id type'})

    def delete_instances(self, instance: Model, related_name: str, ids_for_delete: list):
        self._validate_ids_for_delete(ids_for_delete, related_name)
        objects_for_delete = []
        
        for id_for_delete in ids_for_delete:
            queryset = getattr(instance, related_name)
            obj = queryset.filter(pk=id_for_delete).first()
            if obj is None: raise ValidationError({f'delete_{related_name}': f'id "{id_for_delete}" does not exist'})
            objects_for_delete.append(obj)
                
        for obj in objects_for_delete:
            obj.delete()

    def delete_many_instances(self, instance: Model, fields_for_delete: list):
        for field_for_delete in fields_for_delete:
            ids_for_delete: list = self.initial_data.get(f'delete_{field_for_delete}')
            if ids_for_delete is not None: self.delete_instances(instance, field_for_delete, ids_for_delete)
                




class ManyChildSerializersConsumer(ManyChildSerializers):
    m2m_fields = {}
    m2o_fields = {}

    def get_related_fields_data(self, validated_data):
        return {

            'm2m_fields': {
                m2m_field_name: validated_data.get(m2m_field_name) for m2m_field_name in self.m2m_fields.keys()
            },

            'm2o_fields': {
                m2o_field_name: validated_data.get(m2o_field_name) for m2o_field_name in self.m2o_fields.keys()
            },
            
        }

    def clear_validated_data(self, validated_data):
        for m2m_field_name in [*self.m2m_fields.keys(), *self.m2o_fields.keys()]:
            if validated_data.get(m2m_field_name): validated_data.pop(m2m_field_name)
        return validated_data

    def create_or_update_many_for_many_data(self, instance, data):
        # many to many 
        for m2m_field_name, SerializerClass in self.m2m_fields.items():
            if data[m2m_field_name] is None: continue
            self.create_or_update_many(
                data[m2m_field_name], SerializerClass, getattr(instance, m2m_field_name), 
                {'pk': 'id'}, str(instance.id), m2m_field_name, True
            )    
        # many to one 
        for m2m_field_name, SerializerClass in self.m2o_fields.items():
            if data[m2m_field_name] is None: continue
            self.create_or_update_many(
                data[m2m_field_name], SerializerClass, getattr(instance, m2m_field_name), 
                {'pk': 'id'}, str(instance.id), m2m_field_name, False
            )
    
    def adapt_data_for_update(self, data): return data

    def update(self, instance, validated_data):
        data = self.get_related_fields_data(validated_data)
        self.update_current_instance(instance, self.clear_validated_data(self.adapt_data_for_update(validated_data)))
        self.create_or_update_many_for_many_data(instance, {**data['m2m_fields'], **data['m2o_fields']})
        self.delete_many_instances(instance, [
            *self.m2m_fields.keys(), 
            *self.m2o_fields.keys()
        ])
        return instance
