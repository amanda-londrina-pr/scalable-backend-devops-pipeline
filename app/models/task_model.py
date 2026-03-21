# app/models/task_model.py

from tortoise import fields, models

from app.domain.enums.task_status import TaskStatus


class Task(models.Model):
    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=200)
    description = fields.TextField(null=True)
    status = fields.CharEnumField(TaskStatus, default=TaskStatus.PENDING)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "tasks"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Task(id={self.id}, title={self.title})"
