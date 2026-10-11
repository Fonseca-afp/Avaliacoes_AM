from fastapi import FastAPI, Depends, HTTPException
from bd_connection import get_db_connection
from sqlalchemy import text
from api.schemas import AlunoCreate, AlunoUpdate, TFBUpdate, TFAMUpdate, ACEUpdate, ModalidadeResultadoUpdate
from api.calculos import flex_br_nota, abd_nota, bola_nota, salto_nota, cooper_distancia, cooper_nota, calculo_tempo_final_tfam, converter_min_seg, nota_pista

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

@app.get("/alunos/by_ramo/{ramo}")
def get_alunos_by_ramo(ramo:str, db=Depends(get_db)):
    result = db.execute(text("SELECT * FROM \"Aluno\" WHERE ramo = :ramo "), {"ramo": ramo}).fetchall()
    if result is None:
        raise HTTPException(status_code=404, detail="Nenhum aluno encontrado para o ramo especificado")
    alunos = [dict(row._mapping) for row in result]
    return {"alunos": alunos}

@app.get("/alunos/by_curso_ramo/{ramo}/{curso}")
def get_alunos_by_curso_ramo(ramo:str, curso:str, db=Depends(get_db)):
    result = db.execute(text("SELECT * FROM \"Aluno\" WHERE ramo = :ramo AND curso = :curso"), {"ramo": ramo, "curso": curso}).fetchall()
    if result is None:
        raise HTTPException(status_code=404, detail="Nenhum aluno encontrado para o curso e ramo especificados")
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

    if not existing_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")
    
    nim = existing_aluno.get("nim")
    sexo = existing_aluno.get("sexo")
    ano = existing_aluno.get("ano")

    dados = tfb.model_dump(exclude_unset=True)
    
    """
    Endpoint para calcular as notas do TFB de um aluno.
    """
   
    if "flex_br_rep" in dados:
        flex_br_nota_result = flex_br_nota(db, existing_aluno["sexo"], existing_aluno["ano"], dados["flex_br_rep"])
        dados["flex_br_nota"] = flex_br_nota_result
    if "abd_rep" in dados:
        abd_nota_result = abd_nota(db, existing_aluno["sexo"], existing_aluno["ano"], dados["abd_rep"])
        dados["abd_nota"] = abd_nota_result
    if "bola_dist" in dados:
        bola_nota_result = bola_nota(db, dados["bola_dist"])
        dados["bola_nota"] = bola_nota_result
    if "salto_dist" in dados:
        salto_nota_result = salto_nota(db, existing_aluno["sexo"], dados["salto_dist"])
        dados["salto_nota"] = salto_nota_result
    if "voltas" in dados and "metros" in dados and "pista" in dados:
        cooper_dist = cooper_distancia(dados["voltas"], dados["metros"], dados["pista"])
        cooper_nota_result = cooper_nota(db, existing_aluno["sexo"], existing_aluno["ano"], cooper_dist)
        dados["cooper_nota"] = cooper_nota_result
        dados["cooper_dist"] = cooper_dist
        dados.pop("voltas", None)
        dados.pop("metros", None)
        dados.pop("pista", None)

    result = db.execute(text("SELECT * FROM \"TFB\" WHERE nim = :nim AND tipo_aval = :tipo_aval"), {"nim": nim, "tipo_aval": tipo_aval}).fetchone()

    if result:
        set_clause = ", ".join([f"{key} = :{key}" for key in dados.keys()])
        if set_clause:
            db.execute(
                text(f"UPDATE \"TFB\" SET {set_clause} WHERE nim = :nim AND tipo_aval = :tipo_aval"),
                {**dados, "nim": nim, "tipo_aval": tipo_aval}
            )
            db.commit()
    else:

        # Inserir os dados do TFB no banco de dados 
        colunas = ", ".join(dados.keys())
        valores = ", ".join([f":{key}" for key in dados.keys()])
        db.execute(
            text(f"""
                INSERT INTO "TFB" (nim, tipo_aval, {colunas})
                VALUES (:nim, :tipo_aval, {valores})
            """),
            {
                "nim": nim,
                "tipo_aval": tipo_aval,
                **dados
            }
        )
        db.commit()

    linha_atual = db.execute(
        text("SELECT * FROM \"TFB\" WHERE nim = :nim AND tipo_aval = :tipo_aval"),
        {"nim": nim, "tipo_aval": tipo_aval}
    ).fetchone()

    tfb_dict = dict(linha_atual._mapping) 

    if (tfb_dict["flex_br_nota"] is not None and
        tfb_dict["abd_nota"] is not None and
        tfb_dict["bola_nota"] is not None and
        tfb_dict["salto_nota"] is not None and
        tfb_dict["cooper_nota"] is not None):
        
        nota = (tfb_dict["flex_br_nota"] + tfb_dict["abd_nota"] + 
                tfb_dict["bola_nota"] + tfb_dict["salto_nota"] + tfb_dict["cooper_nota"])/5

        db.execute(text('UPDATE \"TFB\" SET nota= :nota WHERE nim= :nim AND tipo_aval= :tipo_aval'), {"nota": nota, "nim": nim, "tipo_aval": tipo_aval})

    nota_final = db.execute(text("SELECT tipo_aval, nota FROM \"TFB\" WHERE nim = :nim AND tipo_aval IN ('TFB1', 'TFB2')"),{"nim": nim}).fetchall()

    nota_tfb1 = None
    nota_tfb2 = None
    
    if len(nota_final) == 2:
        for row in nota_final:
            if row[0] == "TFB1":
                nota_tfb1 = row[1]
            elif row[0] == "TFB2":
                nota_tfb2 = row[1]

    if nota_tfb1 is not None and nota_tfb2 is not None:
        if ano == 1:
            gin_resultado = db.execute(text("""SELECT mr.nota
                                                FROM "ModalidadeResultado" mr
                                                JOIN "Modalidade" m ON mr.modalidade_id = m.id 
                                                WHERE mr.nim = :nim AND m.nome = 'gin'"""), 
                                            {"nim": nim}
                                        ).fetchone()
            if gin_resultado is None:
                raise HTTPException(status_code=404, detail="Nenhuma nota encontrada para a modalidade Gin do aluno especificado")
            
            nota_final = (0.3*nota_tfb1)+(0.45*nota_tfb2)+(0.25*gin_resultado[0])
        else:
            nota_final = (0.4*nota_tfb1)+(0.6*nota_tfb2)

        result = db.execute(text('SELECT * FROM "TFB_Final" WHERE nim = :nim'),
                            {"nim": nim}).fetchone()
        if result:
            db.execute(text('UPDATE "TFB_Final" SET tfb_final = :tfb_final WHERE nim = :nim'), {"nim": nim, "tfb_final": nota_final})
            db.commit()
        else:
            db.execute(
                text("""
                    INSERT INTO "TFB_Final" (nim, tfb_final)
                    VALUES (:nim, :tfb_final)
                """),
                {
                    "nim": nim,
                    "tfb_final": nota_final
                }
            )
            db.commit()
       
    else:
        raise HTTPException(status_code=404, detail="Não é possível calcular a nota final. Verifique se o alunos tem as notas todas inseridas.")

    

    db.commit()
    return {"message": "Dados do TFB criados com sucesso."}   

@app.post("/alunos/{num_corpo}/modalidade/{nome_modalidade}/{tipo_aval}")
def modalidade_resultado(num_corpo: int, nome_modalidade: str, tipo_aval: str,
                         corpo: ModalidadeResultadoUpdate, db=Depends(get_db)):
    existing_aluno = obter_aluno_by_num_corpo(num_corpo, db)

    if not existing_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")

    nim = existing_aluno.get("nim")
    curso = existing_aluno.get("curso")
    ano = existing_aluno.get("ano")

    modalidade = obter_modalidade(nome_modalidade, db)
    modalidade_id = modalidade["id"]

    # A F311 só se aplica a alunos do curso CAV no 4º ano
    if modalidade["nome"] == "f311":
        if ano != 4 or curso != "CAV":
            raise HTTPException(
                status_code=400,
                detail="A F311 aplica-se apenas a alunos do curso CAV no 4º ano."
            )

    params = {
        "nim": nim,
        "modalidade_id": modalidade_id,
        "tipo_aval": tipo_aval,
        "nota": corpo.nota,
    }

    existente = db.execute(
        text("""
            SELECT id FROM "ModalidadeResultado"
            WHERE nim = :nim AND modalidade_id = :modalidade_id AND tipo_aval = :tipo_aval
        """),
        params
    ).fetchone()

    if existente:
        db.execute(
            text("""
                UPDATE "ModalidadeResultado" SET nota = :nota
                WHERE nim = :nim AND modalidade_id = :modalidade_id AND tipo_aval = :tipo_aval
            """),
            params
        )
    else:
        db.execute(
            text("""
                INSERT INTO "ModalidadeResultado" (nim, modalidade_id, tipo_aval, nota)
                VALUES (:nim, :modalidade_id, :tipo_aval, :nota)
            """),
            params
        )

    db.commit()
    return {"message": "Resultado da modalidade guardado com sucesso."}
        



@app.post("/alunos/{num_corpo}/tfam/{tipo_aval}")
def criar_tfam(num_corpo: int, tipo_aval: str, tfam: TFAMUpdate, db=Depends(get_db)):
    """
        Endpoint para criar os dados do TFAM de um aluno.
        """
        # Verificar se o aluno existe pelo número de corpo
    existing_aluno = obter_aluno_by_num_corpo(num_corpo, db)

    if not existing_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")
    
    nim = existing_aluno.get("nim")
    sexo = existing_aluno.get("sexo")
    ano = existing_aluno.get("ano")

    dados = tfam.model_dump(exclude_unset=True)
    
    """
    Endpoint para calcular as notas do TFAM de um aluno.
    """
    if "tempo_inicio" in dados:
        dados["tempo_inicio"] = converter_min_seg(dados["tempo_inicio"])

    if "tempo_fim" in dados:
        dados["tempo_fim"] = converter_min_seg(dados["tempo_fim"])

    if "acertos" in dados:
        dados["acertos"] = converter_min_seg(dados["acertos"])

    if "tempo_inicio" in dados and "tempo_fim" in dados: 
        dados["tempo_final"] = calculo_tempo_final_tfam(dados["tempo_fim"], dados["tempo_inicio"], dados.get("acertos", 0))
        dados["nota_base"] = nota_pista(db, ano, sexo, dados["tempo_final"])

    result = db.execute(text("SELECT * FROM \"TFAM\" WHERE nim = :nim AND tipo_aval= :tipo_aval"), {"nim": nim, "tipo_aval": tipo_aval}).fetchone()

    if result:
        set_clause = ",".join([f":{key} = :key" for key in dados.keys()])
        db.execute(
            text(f"UPDATE \"TFAM\" SET {set_clause} WHERE nim = :nim AND tipo_aval= :tipo_aval"),
            {**dados, "nim": nim, "tipo_aval": tipo_aval}
        )
        db.commit()
    else:
        colunas = ", ".join(dados.keys())
        valores = ", ".join([f":{key}" for key in dados.keys()])
        db.execute(
            text(f"""
                INSERT INTO "TFAM" (nim, tipo_aval, {colunas})
                VALUES (:nim, :tipo_aval, {valores})
                """),
            {
                "nim": nim,
                "tipo_aval": tipo_aval,
                **dados
            }
        )
        db.commit()
    return {"message": "Dados do TFAM guardados com sucesso."}

@app.get("/alunos/{num_corpo}/tfam")
def get_tfam_by_num_corpo(num_corpo: int, db=Depends(get_db)):
    """
    Função auxiliar para obter os dados do TFB de um aluno pelo número de corpo.
    """
    result = obter_aluno_by_num_corpo(num_corpo, db)
    nim = result.get("nim")
    result = db.execute(text("SELECT * FROM \"TFAM\" WHERE nim = :nim"), {"nim": nim}).fetchall()
    if not result:
        raise HTTPException(status_code=404, detail="Dados do TFAM não encontrados para o aluno especificado")
    return [dict(row._mapping) for row in result]

@app.post("/alunos/{num_corpo}/ace")
def criar_ace(num_corpo: int, ace: ACEUpdate, db=Depends(get_db)):
    """
        Endpoint para criar os dados da(s) ACE's de um aluno.
        """
        # Verificar se o aluno existe pelo número de corpo
    existing_aluno = obter_aluno_by_num_corpo(num_corpo, db)

    if not existing_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")
    
    nim = existing_aluno.get("nim")
    sexo = existing_aluno.get("sexo")
    ano = existing_aluno.get("ano")

    dados = ace.model_dump(exclude_unset=True)
    
    """
    Endpoint para calcular inserir dados das ce's do aluno.
    """
    result = db.execute(text("SELECT * FROM \"ACE\" WHERE nim = :nim"), {nim: nim}).fetchone()

    if result:
        set_clause = ",".join([f":{key} = :{key}" for key in dados.keys()])
        if set_clause:
            db.execute(text(f"UPDATE \"ACE\" SET {set_clause} WHERE nim = :nim"), {**dados, "nim": nim})
            db.commit()
   


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

def obter_modalidade(nome: str, db=Depends(get_db)):
    """
    Função auxiliar para obter uma modalidade pelo nome.
    """
    result = db.execute(text("SELECT * FROM \"Modalidade\" WHERE nome = :nome"), {"nome": nome.lower()}).fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Modalidade não encontrada")
    return dict(result._mapping)
