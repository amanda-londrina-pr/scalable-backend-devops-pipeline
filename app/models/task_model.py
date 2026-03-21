from typing import List

from tortoise import Model, fields


# Database Model
class Task(Model):
    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=200)
    description = fields.TextField(null=True)
    completed = fields.BooleanField(default=False)


class TaskPage:
    def __init__(
            self,
            data: List[Task],
            total: int,
            page: int,
            page_size: int,
            total_pages: int,
    ):
        self.data = data
        self.total = total
        self.page = page
        self.page_size = page_size
        self.total_pages = total_pages
