import pandas as pd
from bd_connection import get_db_connection
from sqlalchemy import text

sep=";"
decimal=","

def importar_pista500():
    """
    Função para importar os dados do Pista 500.
    """
    # Lógica para importar os dados do Pista 500 e armazenar no DataFrame df
    
    # ler ficheiro csv com separador e decimal especificados
    df = pd.read_csv('/home/andre/projetos/Avaliacoes_AM/Avaliacoes_AM/dados/Tabelas_pista500.csv', sep=sep, decimal=decimal) 

    # renomear colunas do DataFrame df
    df = df.rename(columns={"Sexo": "sexo", "Segundos": "segundos", "Nota":"nota"}) 

    # remover coluna "ID" do DataFrame df
    df = df.drop(columns=["id"])

    return df

def inserir_pista500(df):
    """
    Função para inserir os dados do Pista 500 no banco de dados.
    """
    dados = df.to_dict(orient='records')

    engine = get_db_connection()
    if engine is None:
        raise RuntimeError("Falha ao conectar ao banco de dados.")

    with engine.connect() as connection:
        connection.execute(text(
                """
                INSERT INTO "Pista500" (sexo, segundos, nota)
                VALUES (:sexo, :segundos, :nota)
                """),
            dados
        )
                
        connection.commit()  # Confirma a transação após cada inserção
    pass

df = importar_pista500()

inserir_pista500(df)

#print(importar_pista500())


