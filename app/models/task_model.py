from tortoise import Model, fields

class Task(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)