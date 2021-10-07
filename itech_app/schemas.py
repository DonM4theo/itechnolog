from datetime import datetime

from sqlalchemy.sql.sqltypes import VARCHAR, SmallInteger
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
    action_data: datetime 

class Program(BaseModel):
    NrPRM: SmallInteger
    NazwaProgramu: VARCHAR(50)
    KodProgramu: VARCHAR(15)
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
    ProKolor: VARCHAR(50)
    ProCzyOtrzep: bool
    ProCzasWygrz: SmallInteger
    StRozZad: SmallInteger
    CzyAktywny: bool