from tortoise import Model, fields


# Database Model
class Task(Model):
    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=200)
    description = fields.TextField(null=True)
    completed = fields.BooleanField(default=False)
