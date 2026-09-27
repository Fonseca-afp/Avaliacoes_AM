from sqlalchemy import text
from fastapi import HTTPException

def flex_br_nota(db, sexo, ano, flex_br_rep):

    resultado = db.execute(text("SELECT flex_br_nota FROM flex_br WHERE sexo = :sexo AND ano = :ano AND flex_br_rep = :flex_br_rep"), {"sexo": sexo, "ano": ano, "flex_br_rep": flex_br_rep}).fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail="Nenhuma nota encontrada para os parâmetros especificados") 

    return resultado[0]

def abd_nota(db, sexo, ano, abd_rep):

    resultado = db.execute(text("SELECT abd_nota FROM situps WHERE sexo = :sexo AND ano = :ano AND abd_rep = :abd_rep"), {"sexo": sexo, "ano": ano, "abd_rep": abd_rep}).fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail="Nenhuma nota encontrada para os parâmetros especificados") 

    return resultado[0]

def cooper_distancia(voltas, metros, pista = "Amadora"):
    if pista == "Amadora":
        distancia = (voltas * 450) + metros
    elif pista == "Sede":
        distancia = (voltas * 283) + metros
    else:
        raise HTTPException(status_code=400, detail="Tipo de pista inválido. Use 'Amadora' ou 'Sede'.")
    
    return distancia

def cooper_nota(db, sexo, ano, cooper_distancia):

    resultado = db.execute(text("SELECT cooper_nota FROM cooper WHERE sexo = :sexo AND ano = :ano AND cooper_dist = :cooper_dist"), {"sexo": sexo, "ano": ano, "cooper_dist": cooper_distancia}).fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail="Nenhuma nota encontrada para os parâmetros especificados") 

    return resultado[0]

def bola_nota(db, sexo, ano, bola_dist):

    resultado = db.execute(text("SELECT bola_nota FROM bola WHERE sexo = :sexo AND ano = :ano AND bola_dist = :bola_dist"), {"sexo": sexo, "ano": ano, "bola_dist": bola_dist}).fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail="Nenhuma nota encontrada para os parâmetros especificados") 

    return resultado[0]

def salto_nota(db, sexo, ano, salto_dist):

    resultado = db.execute(text("SELECT salto_nota FROM salto WHERE sexo = :sexo AND ano = :ano AND salto_dist = :salto_dist"), {"sexo": sexo, "ano": ano, "salto_dist": salto_dist}).fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail="Nenhuma nota encontrada para os parâmetros especificados") 

    return resultado[0]