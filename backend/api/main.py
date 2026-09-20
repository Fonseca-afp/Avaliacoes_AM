from fastapi import FastAPI, Depends, HTTPException
from bd_connection import get_db_connection
from sqlalchemy import text
from api.schemas import AlunoCreate, AlunoUpdate, TFBUpdate

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

@app.get("/alunos/by_nim/{nim}")
def get_aluno_by_nim(nim: str, db=Depends(get_db)):
    """
    Função auxiliar para obter um aluno pelo NIM.
    """
    result = db.execute(text("SELECT * FROM \"Aluno\" WHERE nim = :nim"), {"nim": nim}).fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return dict(result._mapping)

@app.get("/alunos/by_num_corpo/{num_corpo}")
def get_aluno_by_num_corpo(num_corpo: int, db=Depends(get_db)):
    """
    Função auxiliar para obter um aluno pelo número de corpo.
    """
    return obter_aluno_by_num_corpo(num_corpo, db)

@app.get("/alunos/by_curso_ramo/{ramo}/{curso}")
def get_alunos_by_curso_ramo(ramo:str, curso:str, db=Depends(get_db)):
    result = db.execute(text("SELECT * FROM \"Aluno\" WHERE ramo = :ramo AND curso = :curso"), {"ramo": ramo, "curso": curso}).fetchall()
    if result is None:
        raise HTTPException(status_code=404, detail="Nenhum aluno encontrado para o curso e ramo especificados")
    alunos = [dict(row._mapping) for row in result]
    return {"alunos": alunos}

@app.get("/alunos/by_curso_ramo/{ramo}")
def get_alunos_by_ramo(ramo:str, db=Depends(get_db)):
    result = db.execute(text("SELECT * FROM \"Aluno\" WHERE ramo = :ramo "), {"ramo": ramo}).fetchall()
    if result is None:
        raise HTTPException(status_code=404, detail="Nenhum aluno encontrado para o ramo especificado")
    alunos = [dict(row._mapping) for row in result]
    return {"alunos": alunos}

@app.get("/alunos/by_curso_ramo_ano/{ramo}/{curso}/{ano}")
def get_alunos_by_curso_ramo_ano(ramo:str, curso:str, ano:int, db=Depends(get_db)):
    result = db.execute(text("SELECT * FROM \"Aluno\" WHERE ramo = :ramo AND curso = :curso AND ano = :ano"), {"ramo": ramo, "curso": curso, "ano": ano}).fetchall()
    if result is None:
        raise HTTPException(status_code=404, detail="Nenhum aluno encontrado para o curso, ramo e ano especificados")
    alunos = [dict(row._mapping) for row in result]
    return {"alunos": alunos}

@app.get("/alunos/by_curso/{curso}")
def get_alunos_by_curso(curso:str, db=Depends(get_db)):
    result = db.execute(text("SELECT * FROM \"Aluno\" WHERE curso = :curso"), {"curso": curso}).fetchall()
    if result is None:
        raise HTTPException(status_code=404, detail="Nenhum aluno encontrado para o curso especificado")
    alunos = [dict(row._mapping) for row in result]
    return {"alunos": alunos}

@app.get("/alunos/by_ano/{ano}")
def get_alunos_by_ano(ano:int, db=Depends(get_db)):
    result = db.execute(text("SELECT * FROM \"Aluno\" WHERE ano = :ano"), {"ano": ano}).fetchall()
    if result is None:
        raise HTTPException(status_code=404, detail="Nenhum aluno encontrado para o ano especificado")
    alunos = [dict(row._mapping) for row in result]
    return {"alunos": alunos}

@app.get("/alunos/by_comp/{comp}")
def get_alunos_by_comp(comp:int, db=Depends(get_db)):
    result = db.execute(text("SELECT * FROM \"Aluno\" WHERE comp = :comp"), {"comp": comp}).fetchall()
    if result is None:
        raise HTTPException(status_code=404, detail="Nenhum aluno encontrado para a companhia especificado")
    alunos = [dict(row._mapping) for row in result]
    return {"alunos": alunos}

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

@app.get("/alunos/{num_corpo}/tfb")
def get_tfb_by_num_corpo(num_corpo: int, db=Depends(get_db)):
    """
    Função auxiliar para obter os dados do TFB de um aluno pelo número de corpo.
    """
    result = obter_aluno_by_num_corpo(num_corpo, db)
    nim = result.get("nim")
    result = db.execute(text("SELECT * FROM \"TFB\" WHERE nim = :nim"), {"nim": nim}).fetchall()
    if not result:
        raise HTTPException(status_code=404, detail="Dados do TFB não encontrados para o aluno especificado")
    return [dict(row._mapping) for row in result]

@app.post("/alunos/{num_corpo}/tfb/{tipo_aval}")
def criar_tfb(num_corpo: int, tipo_aval: str, tfb: TFBUpdate, db=Depends(get_db)):
    """
    Endpoint para criar os dados do TFB de um aluno.
    """
    # Verificar se o aluno existe pelo número de corpo
    existing_aluno = obter_aluno_by_num_corpo(num_corpo, db)

    nim = existing_aluno.get("nim")

    if not existing_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")

    result = db.execute(text("SELECT * FROM \"TFB\" WHERE nim = :nim AND tipo_aval = :tipo_aval"), {"nim": nim, "tipo_aval": tipo_aval}).fetchone()

    if result:
        dados_para_atualizar = tfb.model_dump(exclude_unset=True)
        set_clause = ", ".join([f"{key} = :{key}" for key in dados_para_atualizar.keys()])
        if set_clause:
            db.execute(
                text(f"UPDATE \"TFB\" SET {set_clause} WHERE nim = :nim AND tipo_aval = :tipo_aval"),
                {**dados_para_atualizar, "nim": nim, "tipo_aval": tipo_aval}
            )
            db.commit()
        return {"message": "Dados do TFB atualizados com sucesso."}

    # Inserir os dados do TFB no banco de dados
    db.execute(
        text("""
            INSERT INTO "TFB" (nim, tipo_aval, flex_br_rep, abd_rep, bola_dist, salto_dist, cooper_dist)
            VALUES (:nim, :tipo_aval, :flex_br_rep, :abd_rep, :bola_dist, :salto_dist, :cooper_dist)
        """),
        {
            "nim": nim,
            "tipo_aval": tipo_aval,
            "flex_br_rep": tfb.flex_br_rep,
            "abd_rep": tfb.abd_rep,
            "bola_dist": tfb.bola_dist,
            "salto_dist": tfb.salto_dist,
            "cooper_dist": tfb.cooper_dist,
        }
    )
    db.commit()
    return {"message": "Dados do TFB criados com sucesso."}


"""Funções Auxiliares"""

###Função auxiliar para obter um aluno pelo número de corpo
def obter_aluno_by_num_corpo(num_corpo: int, db=Depends(get_db)):
    """
    Função auxiliar para obter um aluno pelo número de corpo.
    """
    result = db.execute(text("SELECT * FROM \"Aluno\" WHERE num_corpo = :num_corpo"), {"num_corpo": num_corpo}).fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return dict(result._mapping)