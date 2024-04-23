import pydantic

class CreateUserSchema(pydantic.BaseModel):
    name: str
    xsxh: str
    password: str
    authcode: int

class OutSchema(pydantic.BaseModel):
    code: int
    tip: str
    name: str
    xsxh: str
    level: int
    class Config():
        orm_mode = True
