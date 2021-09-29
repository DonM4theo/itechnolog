from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'data': {'name': 'Big Don'}}

@app.get('/about')
def about():
    return {'data': 'about page'}

@app.get('/home')
def home():
    return {'data': 'Testowa podstrona'}

@app.post('/add')
def add():
    return None