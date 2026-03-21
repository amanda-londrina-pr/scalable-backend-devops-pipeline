from pydantic import BaseModel


class MetaSchema(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int