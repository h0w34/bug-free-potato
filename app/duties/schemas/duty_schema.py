from marshmallow import Schema, ValidationError, fields, pre_load


class DutySchema(Schema):
    date = fields.Date()
    duty_type_id = fields.Integer()
    cadet_roles_ids = fields.List(fields.Tuple(fields.Integer(), fields.Integer()))
    ...
