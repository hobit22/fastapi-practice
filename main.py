from fastapi import FastAPI

app = FastAPI()

from fastapi.responses import FileResponse
from pydantic import BaseModel

@app.get("/")
def hello():
    return 'hello'


@app.get('/test')
def html_test():
    return FileResponse('index.html')

class Model(BaseModel):
    name: str
    phone: int

@app.post("/send")
def post_test(data: Model):
    print(data)
    return 'post success'