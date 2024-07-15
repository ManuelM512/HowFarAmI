from pydantic import BaseModel


class Links(BaseModel):
    from_link: str
    to_link: str
