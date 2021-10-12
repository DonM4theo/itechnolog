from sqlalchemy.sql.sqltypes import SmallInteger, DateTime
from pydantic import BaseModel, EmailStr
from typing import Optional

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
    action_data: DateTime 
    class Config:
        arbitrary_types_allowed = True

class Program(BaseModel):
    NrPRM: SmallInteger
    NazwaProgramu: str #VARCHAR(50)
    KodProgramu: str #VARCHAR(15)
    CzyProgPrior: bool
    CzyNiepWsad: bool
    CzyUltraM05: bool
    CzyPolewaczka: bool
    KtlPMC: int #SmallInteger
    SzerTraw: int #SmallInteger
    Pow: int #SmallInteger
    CzyOdmuch: int #SmallInteger
    KtlNapPW: int #SmallInteger
    KtlCzasNN: int #SmallInteger
    KtlPRK: int #SmallInteger
    KtlCzasWygrz: int #SmallInteger
    FsfCzasSusz: int #SmallInteger
    Gmp: int #SmallInteger
    CzyMask: int #SmallInteger
    ProPMZad: int #SmallInteger
    ProKolor: str #VARCHAR(50)
    ProCzyOtrzep: bool
    ProCzasWygrz: int #SmallInteger
    StRozZad: int #SmallInteger
    CzyAktywny: bool
    class Config:
        arbitrary_types_allowed = True
        orm_mode =True

class Show_program(BaseModel):
    NrPRM: int #SmallInteger
    NazwaProgramu: str #VARCHAR(50)
    class Config:
        arbitrary_types_allowed = True
        orm_mode =True