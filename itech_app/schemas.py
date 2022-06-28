from typing import Optional
from sqlalchemy.sql.elements import Null
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    login: str
    hashed_password: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str = "UNKNOWN"
    is_active: bool
    can_edit: bool = False
    can_remove: bool = False
    can_create: bool = False
    is_admin: bool = False
    notification: bool = False

class Log(BaseModel):
    sql_query: str
    user_id: int 
    class Config:
        arbitrary_types_allowed = True
        orm_mode =True

class Program(BaseModel):
    NrPRM: int
    NazwaProgramu: str #VARCHAR(50)
    CzyProgPrior: bool = False
    CzyNiepWsad: bool = False
    CzyUltraM05: bool = False
    CzyPolewaczka: bool = False
    KtlPMC: int = 1
    SzerTraw: int = 600
    Pow: int
    CzyOdmuch: int = 0
    KtlNapPW: int
    KtlCzasNN: int = 30
    KtlPRK: int
    KtlCzasWygrz: int = 30
    FsfCzasSusz: Optional[int] = None#= Null
    Gmp: Optional[int] = None #= Null
    CzyMask: Optional[int] = None #= Null
    ProPMZad: Optional[int] = None #= Null
    ProKolor: Optional[int] = None #= Null #VARCHAR(50)
    ProCzyOtrzep: Optional[bool] = None
    ProCzasWygrz: Optional[int] = None #= Null
    StRozZad: int = 1
    CzyAktywny: bool = True
    class Config:
        arbitrary_types_allowed = True
        orm_mode =True
