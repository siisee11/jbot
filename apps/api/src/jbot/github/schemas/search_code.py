from pydantic import BaseModel


class SearchCodeResultSchema(BaseModel):
    content: str
    file_path: str
    fragment: str
