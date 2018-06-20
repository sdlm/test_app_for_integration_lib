from typing import Tuple

from marshmallow import Schema, SchemaOpts, post_load


class ORMModelOpts(SchemaOpts):
    """
    Same as the default class Meta options,
    but adds "model" and "unique" options for enveloping.
    """
    def __init__(self, meta, **kwargs):
        del kwargs
        SchemaOpts.__init__(self, meta)
        for attr_name in ['model', 'unique']:
            value = getattr(meta, attr_name, None)
            setattr(self, attr_name, value)


class DjangoModelSchema(Schema):
    OPTIONS_CLASS = ORMModelOpts

    @post_load
    def make_object(self, data):
        model = self.opts.model

        # noinspection PyProtectedMember
        fields = model._meta.get_fields()

        m2m_fields = self.get_m2m_fields(fields)
        # fk_fields = self.get_fk_fields(fields)

        data, m2m_data = self.separate_data_for_m2m_fields(data, m2m_fields)

        instance, _ = model.objects.get_or_create(**data)

        self.update_m2m_relations(instance, m2m_data)

        return instance

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
    def separate_data_for_m2m_fields(data: dict, fields: list) -> Tuple[dict, dict]:
        data_for_m2m_fields = {}
        for f in fields:
            if f.name in data:
                data_for_m2m_fields[f.name] = data.pop(f.name)
        return data, data_for_m2m_fields

    @staticmethod
    def update_m2m_relations(instance, m2m_data: dict) -> None:
        for field_name, objects in m2m_data.items():
            getattr(instance, field_name).set(objects)


class SQLAlchemyModelSchema(Schema):
    OPTIONS_CLASS = ORMModelOpts

    @post_load
    def make_object(self, data):
        ...


class PeeweeModelSchema(Schema):
    OPTIONS_CLASS = ORMModelOpts

    @post_load
    def make_object(self, data):
        ...


class PonyModelSchema(Schema):
    OPTIONS_CLASS = ORMModelOpts

    @post_load
    def make_object(self, data):
        ...
