from datetime import datetime
from typing import List
from sqlalchemy.sql.schema import ForeignKey
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
    CzyProgPrior: bool
    CzyNiepWsad: bool
    CzyUltraM05: bool
    CzyPolewaczka: bool
    KtlPMC: int
    SzerTraw: int
    Pow: int
    CzyOdmuch: int
    KtlNapPW: int
    KtlCzasNN: int
    KtlPRK: int
    KtlCzasWygrz: int
    FsfCzasSusz: int
    Gmp: int
    CzyMask: int
    ProPMZad: int
    ProKolor: str #VARCHAR(50)
    ProCzyOtrzep: bool
    ProCzasWygrz: int
    StRozZad: int
    CzyAktywny: bool
    class Config:
        arbitrary_types_allowed = True
        orm_mode =True

# class Show_program(BaseModel):
#     NrPRM: int
#     NazwaProgramu: str #VARCHAR(50)
#     class Config:
#         arbitrary_types_allowed = True
#         orm_mode =True