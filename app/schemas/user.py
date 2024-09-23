from marshmallow import Schema, fields, validate
from app.schemas.account import AccountSchema


class UserSchema(Schema):
    id = fields.String()
    name = fields.String(required=True, validate=validate.Length(max=150))
    password = fields.String(required=True, validate=validate.Length(max=255))
    accounts = fields.List(fields.Nested(AccountSchema()))
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    class Meta:
        ordered = True
