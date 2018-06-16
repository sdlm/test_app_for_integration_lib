from marshmallow import Schema, fields


class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()


class TagSchema(Schema):
    name = fields.String()


class PostSchema(Schema):
    title = fields.String()
    text = fields.String()
    author = fields.Integer()
