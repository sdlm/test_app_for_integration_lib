from typing import Tuple, Optional

from django.db.models import QuerySet

from marshmallow_fork.exceptions import InconsistentDataError


class DjangoModelHelper:

    model = None
    fields: list
    original_data: dict

    def __init__(self, model, fields: list, data: dict):
        self.model = model
        self.fields = fields
        self.original_data = data

    def update_instance_if_exists_by_search_by_uniq_fields(self) -> Optional[object]:
        qs_by_uniq_field = self.get_qs_by_uniq_field()
        instance = qs_by_uniq_field.first()
        if instance:
            other_data = self.implement_m2m_data(instance)
            qs_by_uniq_field.update(**other_data)
            instance.refresh_from_db()
            return instance

    def get_or_create_with_care_about_m2m(self):
        m2m_fields = self.get_m2m_fields(self.fields)

        data, m2m_data = self.separate_data_for_m2m_fields(self.original_data, m2m_fields)

        instance, _ = self.model.objects.get_or_create(**data)

        self.update_m2m_relations(instance, m2m_data)

        instance.refresh_from_db()

        return instance

    def get_qs_by_uniq_field(self) -> QuerySet:
        fields_with_unique_constraint = self.get_fields_with_unique_constraint(self.fields)
        if not fields_with_unique_constraint:
            return self.model.objects.none()

        filter_kwargs = self.get_filter_kwargs_by_all_uniq_fields(
            fields_with_unique_constraint=fields_with_unique_constraint,
            data=self.original_data
        )
        if not filter_kwargs:
            return self.model.objects.none()

        pks = set()
        for field_name, value in filter_kwargs.items():
            temp_instance = self.model.objects.filter(**{field_name: value}).first()
            if temp_instance:
                pks.add(temp_instance.pk)
            else:
                pks.add(None)
            if len(pks) > 1:
                raise InconsistentDataError()

        return self.model.objects.filter(**filter_kwargs)

    @staticmethod
    def get_filter_kwargs_by_all_uniq_fields(fields_with_unique_constraint, data):
        filter_kwargs = {}
        for field in fields_with_unique_constraint:
            value = data.get(field.name)
            if not value:
                continue
            filter_kwargs[field.name] = value
        return filter_kwargs

    def implement_m2m_data(self, instance) -> dict:
        m2m_fields = self.get_m2m_fields(self.fields)
        other_data, m2m_data = self.separate_data_for_m2m_fields(self.original_data, m2m_fields)
        self.update_m2m_relations(instance, m2m_data)
        return other_data

    @staticmethod
    def get_fields_with_unique_constraint(fields: list) -> list:
        return [
            f for f in fields
            if not f.auto_created and not f.is_relation and hasattr(f, 'unique') and f.unique
        ]

    @staticmethod
    def get_m2m_fields(fields: list) -> list:
        return [
            f for f in fields
            if f.many_to_many and not f.auto_created
        ]

    @staticmethod
    def get_fk_fields(fields: list) -> list:
        return [
            f for f in fields
            if (f.one_to_many or f.one_to_one) and not f.auto_created
        ]

    @staticmethod
    def separate_data_for_m2m_fields(data: dict, m2m_fields: list) -> Tuple[dict, dict]:
        temp_data = data.copy()
        data_for_m2m_fields = {}
        for f in m2m_fields:
            if f.name in data:
                data_for_m2m_fields[f.name] = temp_data.pop(f.name)
        return temp_data, data_for_m2m_fields

    @staticmethod
    def update_m2m_relations(instance, m2m_data: dict) -> None:
        for field_name, objects in m2m_data.items():
            getattr(instance, field_name).set(objects)
