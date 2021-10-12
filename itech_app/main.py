from fastapi import FastAPI, Depends, HTTPException, status
import schemas, models
from hashing import Hash
from DB_App import Appengine, AppSessionLocal
from DB_Server import Serverengine, ServerSessionLocal
from sqlalchemy.orm import Session

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

@app.post('/register')
def register(request: schemas.User, db: Session = Depends(get_db_conn_App)):
    new_user = models.User(login=request.login, hashed_password=Hash.bcrypt(request.hashed_password),
    first_name=request.first_name, last_name=request.last_name, email=request.email,
    phone_number=request.phone_number, is_active=request.is_active, can_edit=request.can_edit,
    can_remove=request.can_remove, can_create=request.can_create, is_admin=request.is_admin,
    notification=request.notification)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/register')
def show_registered(db: Session = Depends(get_db_conn_App)):
    users = db.query(models.User).all()
    return users

#######################################################################################################################
#######################################################################################################################
#DB_Server#############################################################################################################

@app.get('/programs')
def get_programs(db: Session = Depends(get_db_conn_Server)):
    programs = db.query(models.Program).all()
    return programs

@app.get('/programs/{NrPRM}')
def get_program_id(NrPRM:int, db: Session = Depends(get_db_conn_Server)):
    program = db.query(models.Program).filter(models.Program.NrPRM == NrPRM).first()
    if not program:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Program o numerze programu malowania:{NrPRM}, nie istnieje.")
    return program