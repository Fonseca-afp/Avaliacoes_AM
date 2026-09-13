from fastapi import FastAPI, Depends
from bd_connection import get_db_connection
from sqlalchemy import text

app = FastAPI()

def get_db():
    
    engine = get_db_connection()
    if engine is None:
        raise RuntimeError("Falha ao conectar ao banco de dados.")
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()

@app.get("/alunos")

def listar_alunos(db=Depends(get_db)):
    """
    Endpoint para listar todos os alunos.
    """
    result = db.execute(text("SELECT * FROM \"Aluno\"")).fetchall()
    alunos = [dict(row._mapping) for row in result]
    return {"alunos": alunos}