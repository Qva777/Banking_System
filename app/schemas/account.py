from marshmallow import Schema, fields, validate


class AccountSchema(Schema):
    id = fields.String()
    account_number = fields.String(required=True, validate=validate.Length(max=16))
    balance = fields.Float()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
