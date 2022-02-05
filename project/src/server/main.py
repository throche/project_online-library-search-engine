from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:4200"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/search")
def read_item(q: str):

    
    return {"res":[{"id": "10001", "Title" : "Apocolocyntosis", "Author": "Lucius Seneca", "Release_Date":"November 10, 2003", "score": "40"},
    	           {"id": "10010", "Title" : "The Eulogies of Howard", "Author": "William Hayley", "Release_Date":"November 7, 2003", "score": "15"},
    	           {"id": "10024", "Title" : "Beneath the Banner", "Author": "F. J. Cross", "Release_Date":"November 9, 2003", "score": "190"}]}
