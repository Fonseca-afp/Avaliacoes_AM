from fastapi import FastAPI, Depends, HTTPException
from bd_connection import get_db_connection
from sqlalchemy import text
from api.schemas import AlunoCreate, AlunoUpdate, TFBCreate, TFBUpdate

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

@app.get("/alunos/by-num-corpo/{num_corpo}")
def get_aluno_by_num_corpo(num_corpo: int, db=Depends(get_db)):
    """
    Função auxiliar para obter um aluno pelo número de corpo.
    """
    result = db.execute(text("SELECT * FROM \"Aluno\" WHERE num_corpo = :num_corpo"), {"num_corpo": num_corpo}).fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return dict(result._mapping)

@app.post("/alunos")
def criar_aluno(aluno: AlunoCreate, db=Depends(get_db)):
    """
    Endpoint para criar um novo aluno.
    """
    # Verificar se o aluno já existe pelo nim
    existing_aluno = db.execute(text("SELECT * FROM \"Aluno\" WHERE nim = :nim"), {"nim": aluno.nim}).fetchone()
    existing_cod_aluno = db.execute(text("SELECT * FROM \"Aluno\" WHERE cod_aluno = :cod_aluno"), {"cod_aluno": aluno.cod_aluno}).fetchone()
    existing_num_corpo = db.execute(text("SELECT * FROM \"Aluno\" WHERE num_corpo = :num_corpo"), {"num_corpo": aluno.num_corpo}).fetchone()

    if existing_aluno:
        raise HTTPException(status_code=400, detail="Aluno com este NIM já existe.")
    if existing_cod_aluno:
        raise HTTPException(status_code=400, detail="Aluno com este código de aluno já existe.")
    if existing_num_corpo:
        raise HTTPException(status_code=400, detail="Aluno com este número de corpo já existe.")

    # Inserir o novo aluno no banco de dados
    db.execute(
        text("""
            INSERT INTO "Aluno" (nim, cod_aluno, num_corpo, ano, comp, posto, nome, ramo, curso, sexo, data_nascimento, altura, peso)
            VALUES (:nim, :cod_aluno, :num_corpo, :ano, :comp, :posto, :nome, :ramo, :curso, :sexo, :data_nascimento, :altura, :peso)
        """),
        {
            "nim": aluno.nim,
            "cod_aluno": aluno.cod_aluno,
            "num_corpo": aluno.num_corpo,
            "ano": aluno.ano,
            "comp": aluno.comp,
            "posto": aluno.posto,
            "nome": aluno.nome,
            "ramo": aluno.ramo,
            "curso": aluno.curso,
            "sexo": aluno.sexo,
            "data_nascimento": aluno.data_nascimento,
            "altura": aluno.altura,
            "peso": aluno.peso
        }
    )
    db.commit()
    return {"message": "Aluno criado com sucesso."}

@app.put("/alunos/{num_corpo}")
def atualizar_aluno(num_corpo: int, aluno: AlunoUpdate, db=Depends(get_db)):
    """
    Endpoint para atualizar os dados de um aluno existente.
    """
    # Verificar se o aluno existe pelo número de corpo
    existing_aluno = db.execute(text("SELECT * FROM \"Aluno\" WHERE num_corpo = :num_corpo"), {"num_corpo": num_corpo}).fetchone()
    if not existing_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")

    # Atualizar os campos fornecidos
    dados_para_atualizar = aluno.model_dump(exclude_unset=True)
    set_clause = ", ".join([f"{key} = :{key}" for key in dados_para_atualizar.keys()])
    if set_clause:
        db.execute(
            text(f"UPDATE \"Aluno\" SET {set_clause} WHERE num_corpo = :num_corpo"),
            {**dados_para_atualizar, "num_corpo": num_corpo}
        )
        db.commit()
    return {"message": "Aluno atualizado com sucesso."}