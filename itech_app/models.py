from sqlalchemy.sql.sqltypes import DATETIME, VARCHAR, SmallInteger
from DB_App import AppBase
from DB_Server import ServerBase
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import defaultload, relationship

class User(AppBase):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    logs = relationship("Log", back_populates="modifier")

class Log(AppBase):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    sql_query = Column(String)
    dt = Column(DATETIME)
    user_id = Column(Integer, ForeignKey("users.id"))

    modifier = relationship("User", back_populates="logs")

class Program(ServerBase):
    __tablename__ = "programy"
    idPRM = Column(Integer, primary_key=True, index=True)
    NrPRM = Column(SmallInteger)
    NazwaProgramu = Column(VARCHAR(50))
    KodProgramu = Column(VARCHAR(15))
    CzyProgPrior = Column(Boolean)
    CzyNiepWsad = Column(Boolean)
    CzyUltraM05 = Column(Boolean)
    CzyPolewaczka = Column(Boolean)
    KtlPMC = Column(SmallInteger)
    SzerTraw = Column(SmallInteger)
    Pow = Column(SmallInteger)
    CzyOdmuch = Column(SmallInteger)
    KtlNapPW = Column(SmallInteger)
    KtlCzasNN = Column(SmallInteger)
    KtlPRK = Column(SmallInteger)
    KtlCzasWygrz = Column(SmallInteger)
    FsfCzasSusz = Column(SmallInteger)
    Gmp = Column(SmallInteger)
    CzyMask = Column(SmallInteger)
    ProPMZad = Column(SmallInteger)
    ProKolor = Column(VARCHAR(50))
    ProCzyOtrzep = Column(Boolean)
    ProCzasWygrz = Column(SmallInteger)
    StRozZad = Column(SmallInteger)
    CzyAktywny = Column(Boolean)
    DataMod = Column(DATETIME)
