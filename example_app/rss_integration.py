from marshmallow import Schema, fields


class EntryTagSchema(Schema):
    name = fields.String(attribute='term')


class EntrySchema(Schema):
    title = fields.String()
    text = fields.String(attribute='summary')
    author = fields.String()
    tags = fields.Nested(EntryTagSchema, many=True)
    url = fields.Url(attribute='link')
