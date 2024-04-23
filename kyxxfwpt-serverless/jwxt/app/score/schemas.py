import pydantic
from typing import List
class SearchScoreSchema(pydantic.BaseModel):
    semester: int
    
class OutSchema(pydantic.BaseModel):
    code: int
    tip: str
    class Config():
        orm_mode = True
class OutScoreSchema(OutSchema):
    gdp_string: str
    table: List[str]
    class Config():
        orm_mode = True