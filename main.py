from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'data': {'name': 'Big Don'}}

@app.get('/program')
def show_list(limit=25, checked: bool=False):
    if checked:
        return {'data': f'lista sprawdzonych programów: {limit} ze 100.'}
    else:
        return {'data': f'lista wszystkich programów: {limit} ze 100.'}

@app.get('/blog/{id}')
def show(id: int):
    return {'data': id}

@app.post('/add')
def add():
    return None