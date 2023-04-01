from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from mongo import Mongo
#from cryptography.fernet import Fernet


# cipher_key = b'key'
# cipher = Fernet(cipher_key)
#print(cipher_key)

app = FastAPI()

class Token(BaseModel):
    token: str

@app.post("/login")
async def get_token(data: str):
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


@app.on_event('startup')
async def start_app():
    await Mongo.fill_db()
