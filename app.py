from fastapi import FastAPI, HTTPException, Header, Body
from pydantic import BaseModel
from mongo import Mongo
from fastapi.middleware.cors import CORSMiddleware
#from loguru import logger
#from cryptography.fernet import Fernet


# cipher_key = b'key'
# cipher = Fernet(cipher_key)
#print(cipher_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PATCH", "DELETE", "PUT"],
    allow_headers=["*"],
)

class Token(BaseModel):
    token: str

@app.post("/login")
async def get_token(data: str = Body(...,embed=True)):
    """Получение токена компании по ИНН"""
    try:
        if company := await Mongo.find_company(tin=data):
            #text = data.encode()
            return Token(token = f'{data}_1234')
    except ValueError:
        raise HTTPException(status_code=403, detail="Неправильный ИНН")
    
@app.get("/me")
async def get_user(token: str = Header()):
    tin = token.split('_')[0]
    #cipher.decrypt(token)
    try:
        if company := await Mongo.find_company(tin=tin):
            return company
    except ValueError:
        raise HTTPException(status_code=403, detail="Неправильный ИНН")
    
@app.get("/chart/win")
async def get_chart_data_win(token: str = Header()):
    tin = token.split('_')[0]
    return await Mongo.get_chart_data_win(tin=tin)

@app.get("/chart/all")
async def get_chart_data_all(token: str = Header()):
    tin = token.split('_')[0]
    return await Mongo.get_chart_data_all(tin=tin)

@app.get("/chart/sum")
async def get_chart_data_sum(token: str = Header()):
    tin = token.split('_')[0]
    return await Mongo.get_chart_data_sum(tin=tin)


@app.on_event('startup')
async def start_app():
    await Mongo.fill_db()
#    logger.info(await Mongo.find_fake_data())
