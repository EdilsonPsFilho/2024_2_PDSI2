from fastapi import FastAPI, status, Depends
from fastapi.params import Body
import classes
import model
from database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Vampas"}

@app.get("/quadrado/{num}")
def square (num: int):
    return num ** 2

# @app.post("/criar")
# def criar_valores(res: dict = Body(...)):
#     print(res)
#     return {"Mensagem": f"Roda: {res['Roda']} Porque: {res['Porque']}"}

#@app.post("/criar")
#def criar_valores(nova_mensagem: classes.Mensagem):
#    print(nova_mensagem)
#    return {"Mensagem": f"Título: {nova_mensagem.titulo} Conteúdo: {nova_mensagem.conteudo} Publicada: {nova_mensagem.publicada}"}

#@app.post("/criar", status_code=status.HTTP_201_CREATED)
#def criar_valores(nova_mensagem: classes.Mensagem, db: Session = Depends(get_db)):
#    mensagem_criada = model.Model_Mensagem(**nova_mensagem.model_dump())
#    db.add(mensagem_criada)
#    db.commit()
#    db.refresh(mensagem_criada)
#    return {"Mensagem": mensagem_criada}