import typing as t

from pydantic import BaseModel, Field


class body(BaseModel):
    param_name: str
    required: bool
    type: str
    description: str = Field(default="")
    format: t.Optional[str]
    value_range: t.Optional[t.List[str]]
    note: t.Optional[str]
    # arbitrary types allowed


class Endpoint(BaseModel):
    type: str
    body: t.Optional[t.List["body"]]
    url: t.Optional[str]
    request: t.Optional[str]
    response: t.Optional[str]
