from datetime import datetime
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import SmallInteger
from sqlalchemy.sql.functions import now
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
    dt:datetime = now
    user_id: int 
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
    KtlPMC: SmallInteger
    SzerTraw: SmallInteger
    Pow: SmallInteger
    CzyOdmuch: SmallInteger
    KtlNapPW: SmallInteger
    KtlCzasNN: SmallInteger
    KtlPRK: SmallInteger
    KtlCzasWygrz: SmallInteger
    FsfCzasSusz: SmallInteger
    Gmp: SmallInteger
    CzyMask: SmallInteger
    ProPMZad: SmallInteger
    ProKolor: str #VARCHAR(50)
    ProCzyOtrzep: bool
    ProCzasWygrz: SmallInteger
    StRozZad: SmallInteger
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