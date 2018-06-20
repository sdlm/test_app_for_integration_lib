from marshmallow import Schema, SchemaOpts, post_load

from marshmallow_fork.classes import DjangoModelHelper
from marshmallow_fork.exceptions import InconsistentDataError


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

        model, fields = self.get_model_and_fields()

        helper = DjangoModelHelper(model=model, fields=fields, data=data)

        try:
            instance = helper.update_instance_if_exists_by_search_by_uniq_fields()
        except InconsistentDataError:
            return None
        if instance:
            return instance

        return helper.get_or_create_with_care_about_m2m()

    def get_model_and_fields(self):
        model = self.opts.model

        # noinspection PyProtectedMember
        fields = model._meta.get_fields()

        return model, fields


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
