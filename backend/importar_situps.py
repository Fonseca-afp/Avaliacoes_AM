import pandas as pd
from bd_connection import get_db_connection
from sqlalchemy import text

sep=";"
decimal=","

def importar_situps():
    """
    Função para importar os dados do SITUPS.
    """
    # Lógica para importar os dados do SITUPS e armazenar no DataFrame df
    
    # ler ficheiro csv com separador e decimal especificados
    df = pd.read_csv('/home/andre/projetos/Avaliacoes_AM/Avaliacoes_AM/dados/Tabelas_situps.csv', sep=sep, decimal=decimal) 

    # renomear colunas do DataFrame df
    df = df.rename(columns={"Ano": "ano", "Sexo": "sexo", "Abd_Rep": "abd_rep", "Abd_Nota":"abd_nota"}) 

    # remover coluna "ID" do DataFrame df
    df = df.drop(columns=["ID"])

    return df

def inserir_situps(df):
    """
    Função para inserir os dados do SITUPS no banco de dados.
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
                INSERT INTO "situps" (ano, sexo, abd_rep, abd_nota)
                VALUES (:ano, :sexo, :abd_rep, :abd_nota)
                """),
            dados
        )
                
        connection.commit()  # Confirma a transação após cada inserção
    pass

df = importar_situps()

inserir_situps(df)
