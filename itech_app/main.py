from sqlalchemy.sql.functions import mode
from fastapi import FastAPI, Depends, HTTPException, status, Response
import schemas, models
from hashing import Hash
from DB_App import Appengine, AppSessionLocal
from DB_Server import Serverengine, ServerSessionLocal, db_URL
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import exc
import pyodbc
from fastapi.responses import HTMLResponse

app = FastAPI()

models.AppBase.metadata.create_all(Appengine)

def get_db_conn_App():
    db = AppSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_conn_Server():
    db = ServerSessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def index():
    return 'Witaj na stronie startowej aplikacji ITechnolog'

#######################################################################################################################
#######################################################################################################################
#DB_App################################################################################################################

@app.post('/register', status_code=status.HTTP_201_CREATED, tags=["users"])
def register(request: schemas.User, db: Session = Depends(get_db_conn_App)):
    new_user = models.User(login=request.login, hashed_password=Hash.bcrypt(request.hashed_password),
            first_name=request.first_name, last_name=request.last_name, email=request.email,
            phone_number=request.phone_number, is_active=request.is_active, can_edit=request.can_edit,
            can_remove=request.can_remove, can_create=request.can_create, is_admin=request.is_admin,
            notification=request.notification)
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except exc.IntegrityError:
        #db.rollback()
        raise HTTPException(status_code=200,
                            detail="Pole Login już istnieje w systemie.")


@app.get('/register', tags=["users"])
def show_registered(db: Session = Depends(get_db_conn_App)):
    users = db.query(models.User).all()
    return users

@app.post('/logs', tags=["users"])
def create_log(request: schemas.Log, db: Session = Depends(get_db_conn_App)):
    new_log = models.Log(sql_query=request.sql_query, dt=datetime.now(), user_id=request.user_id)
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

@app.get('/logs/{user_id}', status_code=200, tags=["users"])
def list_user_changes(user_id:int, db: Session = Depends(get_db_conn_App)):
    logs = db.query(models.Log.id, models.Log.sql_query, models.User.login, models.Log.dt).filter((models.Log.user_id == user_id)).join(models.User).all()
    if not logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Użytkownik o podanym id:{user_id}, nie istnieje. Lub użytkownik nie posiada, żadnej historii wprowadzanych zmian.")
    return logs

@app.put('/register/{user_id}', status_code=status.HTTP_202_ACCEPTED,  tags=["users"])
def update(user_id:int, request: schemas.User, db: Session = Depends(get_db_conn_App)):
    user = db.query(models.User).filter(models.User.id == user_id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Program o id: {user_id}, nie istnieje")
    user.update(request.dict())
    db.commit()
    return 'record updated'

@app.delete('/register/{user_id}', tags=["users"])
def destroy(user_id:int, db: Session = Depends(get_db_conn_App)):
    
    db.query(models.User).filter(models.User.id == user_id).delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#######################################################################################################################
#######################################################################################################################
#DB_Server#############################################################################################################

@app.get('/programs', tags=["programs"])
def get_programs(db: Session = Depends(get_db_conn_Server)):
    programs = db.query(models.Program).all()
    html_content = """    
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>View04</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            <style>
                body {
                    height: 100%;
                    padding: 0;
                    margin: 0;
                }

                div {
                    position:fixed;
                    width: 50%;
                    height: 100%;
                }

                #NW { top:0;   left:0;   background:rgba(22, 1, 211, 0.904)}
                #NE { top:0;   left:50%; background:rgb(73, 144, 202)}
                #SW { top:50%; left:0;   background:rgba(6, 88, 6, 0.836)}
                #SE { top:50%; left:50%; background:rgb(4, 190, 29) }
            </style>
        </head>
        <body>
            <div id="NW"></div>
            <div id="NE"></div>
        
        <script>

        </script>
        </body>
        </html>
        """
    return HTMLResponse(content=html_content, status_code=200)

@app.get('/programs/{NrPRM}', tags=["programs"])
def get_program_by_NrPRM(NrPRM:int, db: Session = Depends(get_db_conn_Server)):
    program = db.query(models.Program).filter(models.Program.NrPRM == NrPRM).first()
    if not program:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Program o numerze programu malowania:{NrPRM}, nie istnieje.")
    return program

@app.post('/programs', tags=["programs"])
def create_program(request: schemas.Program):
    
    try:
        conn = pyodbc.connect(db_URL)
        print("Connected")
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO [dbo].[programy](
        [NrPRM], [NazwaProgramu], [CzyProgPrior], [CzyNiepWsad], [CzyUltraM05], [CzyPolewaczka], [KtlPMC],
        [SzerTraw], [Pow], [CzyOdmuch], [KtlNapPW], [KtlCzasNN], [KtlPRK], [KtlCzasWygrz], [FsfCzasSusz], 
        [Gmp], [CzyMask], [ProPMZad], [ProKolor], [ProCzyOtrzep], [ProCzasWygrz], [StRozZad], [CzyAktywny])
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
          
        request.NrPRM,request.NazwaProgramu,request.CzyProgPrior,request.CzyNiepWsad,request.CzyUltraM05,request.CzyPolewaczka,request.KtlPMC,
        request.SzerTraw,request.Pow,request.CzyOdmuch,request.KtlNapPW,request.KtlCzasNN,request.KtlPRK,request.KtlCzasWygrz,request.FsfCzasSusz,
        request.Gmp,request.CzyMask,request.ProPMZad,request.ProKolor,request.ProCzyOtrzep,request.ProCzasWygrz,request.StRozZad,request.CzyAktywny)

        conn.commit()   
        conn.close()

        return("Insert completed")
    
    except exc.IntegrityError:
        conn.close()
        raise HTTPException(status_code=200,
                            detail="Rekord nie został stworzyny. Błąd wprowadzonych danych")
        
@app.put('/programs/{idPRM}', status_code=status.HTTP_202_ACCEPTED,  tags=["programs"])
def update(idPRM:int, request: schemas.Program, db: Session = Depends(get_db_conn_Server)):
    program = db.query(models.Program).filter(models.Program.idPRM == idPRM)
    if not program.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Program o id: {idPRM}, nie istnieje")
    program.update(request.dict())
    db.commit()
    return 'record updated'

@app.delete('/programs/{idPRM}', tags=["programs"])
def destroy(idPRM:int, db: Session = Depends(get_db_conn_Server)):
    
    db.query(models.Program).filter(models.Program.idPRM == idPRM).delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    




# @app.get('/prog', tags=["programs"])
# def read():
    
#     try:
#         conn = pyodbc.connect(db_URL)
#         print("Read")
#         cursor = conn.cursor()
#         cursor.execute("select * from dbo.programy")
#         for row in cursor:
#             a = print(f'row = {row}')
#         conn.close()
#         return(a)
#     except:
#         return(print("Nieudane połączenie"))


# @app.post('/programs', tags=["programs"])
# def create_program(request: schemas.Program, db: Session = Depends(get_db_conn_Server)):
#     new_program = models.Program(NrPRM=request.NrPRM, NazwaProgramu=request.NazwaProgramu, CzyProgPrior=request.CzyProgPrior, CzyNiepWsad=request.CzyNiepWsad,
#                 CzyUltraM05=request.CzyUltraM05, CzyPolewaczka=request.CzyPolewaczka, KtlPMC=request.KtlPMC, SzerTraw=request.SzerTraw, Pow=request.Pow,
#                 CzyOdmuch=request.CzyOdmuch, KtlNapPW=request.KtlNapPW, KtlCzasNN=request.KtlCzasNN, KtlPRK=request.KtlPRK, KtlCzasWygrz=request.KtlCzasWygrz,
#                 FsfCzasSusz=request.FsfCzasSusz, Gmp=request.Gmp, CzyMask=request.CzyMask, ProPMZad=request.ProPMZad, ProKolor=request.ProKolor,
#                 ProCzyOtrzep=request.ProCzyOtrzep, ProCzasWygrz=request.ProCzasWygrz, StRozZad=request.StRozZad, CzyAktywny=request.CzyAktywny)
#     try:
#         db.add(new_program)
#         db.commit()
#         db.refresh(new_program)
#         return new_program
#     except exc.IntegrityError:
#         #db.rollback()
#         raise HTTPException(status_code=200,
#                             detail="Rekord nie został stworzyny.")
                           