from fastapi import FastAPI, Depends, HTTPException, status
import schemas, models
from hashing import Hash
from DB_App import Appengine, AppSessionLocal
from DB_Server import Serverengine, ServerSessionLocal
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import exc

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
#######################################################################################################################
#######################################################################################################################
#DB_Server#############################################################################################################

@app.get('/programs', tags=["programs"])
def get_programs(db: Session = Depends(get_db_conn_Server)):
    programs = db.query(models.Program).all()
    return programs

@app.get('/programs/{NrPRM}', tags=["programs"])
def get_program_by_NrPRM(NrPRM:int, db: Session = Depends(get_db_conn_Server)):
    program = db.query(models.Program).filter(models.Program.NrPRM == NrPRM).first()
    if not program:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Program o numerze programu malowania:{NrPRM}, nie istnieje.")
    return program

