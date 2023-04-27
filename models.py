from tortoise import fields
from tortoise.models import Model


class Tennis(Model):
    id = fields.IntField(pk=True)
    event_id = fields.CharField(16, index=True)
    day = fields.CharField(16, null=True)
    month = fields.CharField(16, null=True)
    year = fields.CharField(16, null=True)
    time = fields.CharField(8)
    tour = fields.CharField(128)
    tour2 = fields.CharField(128)
    step = fields.CharField(128, null=True)
    p1 = fields.CharField(128)
    p2 = fields.CharField(128)

    r1 = fields.CharField(32, null=True)
    r2 = fields.CharField(32, null=True)

    team_1_set_1 = fields.IntField(null=True)
    team_1_set_1_break = fields.IntField(null=True)
    team_1_set_2 = fields.IntField(null=True)
    team_1_set_2_break = fields.IntField(null=True)
    team_1_set_3 = fields.IntField(null=True)
    team_1_set_3_break = fields.IntField(null=True)
    team_1_set_4 = fields.IntField(null=True)
    team_1_set_4_break = fields.IntField(null=True)
    team_1_set_5 = fields.IntField(null=True)
    team_1_set_5_break = fields.IntField(null=True)

    team_2_set_1 = fields.IntField(null=True)
    team_2_set_1_break = fields.IntField(null=True)
    team_2_set_2 = fields.IntField(null=True)
    team_2_set_2_break = fields.IntField(null=True)
    team_2_set_3 = fields.IntField(null=True)
    team_2_set_3_break = fields.IntField(null=True)
    team_2_set_4 = fields.IntField(null=True)
    team_2_set_4_break = fields.IntField(null=True)
    team_2_set_5 = fields.IntField(null=True)
    team_2_set_5_break = fields.IntField(null=True)

    status = fields.CharField(128, null=True)
    full_time = fields.CharField(16, null=True)
    set_1_time = fields.CharField(16, null=True)
    set_2_time = fields.CharField(16, null=True)
    set_3_time = fields.CharField(16, null=True)
    set_4_time = fields.CharField(16, null=True)
    set_5_time = fields.CharField(16, null=True)

    c1 = fields.FloatField(null=True)
    c2 = fields.FloatField(null=True)
    fs1 = fields.CharField(16, null=True)
    fs2 = fields.CharField(16, null=True)

