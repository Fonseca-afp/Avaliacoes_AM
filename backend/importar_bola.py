import pandas as pd
from bd_connection import get_db_connection
from sqlalchemy import text

sep=";"
decimal=","

def importar_bola():
    """
    Função para importar os dados do Bola.
    """
    # Lógica para importar os dados do Bola e armazenar no DataFrame df
    
    # ler ficheiro csv com separador e decimal especificados
    df = pd.read_csv('/home/andre/projetos/Avaliacoes_AM/Avaliacoes_AM/dados/Tabelas_bola.csv', sep=sep, decimal=decimal) 

    # renomear colunas do DataFrame df
    df = df.rename(columns={"Bola_Dist": "bola_dist", "Bola_Nota":"bola_nota"}) 

    # remover coluna "ID" do DataFrame df
    df = df.drop(columns=["ID"])

    return df

def inserir_bola(df):
    """
    Função para inserir os dados do Bola no banco de dados.
    """
    # Lógica para inserir os dados do DataFrame df no banco de dados
    # Exemplo: df.to_sql('nome_da_tabela', con=engine, if_exists='replace', index=False)
    dados = df.to_dict(orient='records')

    engine = get_db_connection()
    if engine is None:
        raise RuntimeError("Falha ao conectar ao banco de dados.")

    with engine.connect() as connection:
        connection.execute(text(
                """
                INSERT INTO "bola" (bola_dist, bola_nota)
                VALUES (:bola_dist, :bola_nota)
                """),
            dados
        )
                
        connection.commit()  # Confirma a transação após cada inserção
    pass

df = importar_bola()

inserir_bola(df)