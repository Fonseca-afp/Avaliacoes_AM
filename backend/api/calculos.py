from sqlalchemy import text
from fastapi import HTTPException
from datetime import time

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

def bola_nota(db, bola_dist):

    resultado = db.execute(text("SELECT bola_nota FROM bola WHERE bola_dist = :bola_dist"), {"bola_dist": bola_dist}).fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail="Nenhuma nota encontrada para os parâmetros especificados") 

    return resultado[0]

def salto_nota(db, sexo, salto_dist):

    resultado = db.execute(text("SELECT salto_nota FROM salto WHERE sexo = :sexo AND salto_dist = :salto_dist"), {"sexo": sexo, "salto_dist": salto_dist}).fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail="Nenhuma nota encontrada para os parâmetros especificados") 

    return resultado[0]

def tabela_pista_ano(ano):

    if ano == 1:
        return "Pista200"

    elif ano == 2:
        return "Marcor"        
    
    elif ano == 3:
        return "Pista500m"

    elif ano == 4:
        return "PistaTriatlo"
    
    else:
        raise HTTPException(status_code=404, detail="Nenhuma tabela encontrada para o ano indicado") 

def nota_pista (db, ano, sexo, segundos):
    tabela = tabela_pista_ano(ano)

    resultado = db.execute(text(f'SELECT nota FROM "{tabela}" WHERE sexo= :sexo AND segundos= :segundos'),{"sexo": sexo, "segundos": segundos}).fetchone()
    if resultado is None:
        raise HTTPException(status_code=404, detail="Nenhuma nota encontrada para os parâmertos especificados")
    
    return resultado [0]

def calculo_tempo_final_tfam(tempo_fim, tempo_inicio, acertos):

    if tempo_inicio is None or tempo_fim is None:
        raise HTTPException(status_code=400, detail="Tempo de pista inválido.")
        
    tempo_final = tempo_fim - tempo_inicio + acertos

    return tempo_final

def converter_min_seg (tempo):
    return (tempo.hour *3600) + (tempo.minute * 60) + tempo.second
