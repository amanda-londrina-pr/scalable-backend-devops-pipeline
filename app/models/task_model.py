from tortoise import Model, fields

class Task(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=50)