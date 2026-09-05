import pandas as pd
from bd_connection import get_db_connection
from sqlalchemy import text


sep=";"
decimal=","

def importar_flex_br():
    """
    Função para importar os dados do Flex BR.
    """
    # Lógica para importar os dados do Flex BR e armazenar no DataFrame df
    
    # ler ficheiro csv com separador e decimal especificados
    df = pd.read_csv('/home/andre/projetos/Avaliacoes_AM/Avaliacoes_AM/dados/Tabelas TFB_BD.csv', sep=sep, decimal=decimal) 

    # renomear colunas do DataFrame df
    df = df.rename(columns={"Ano": "ano", "Sexo": "sexo", "Flex_Rep": "flex_br_rep", "Flex_Nota":"flex_br_nota"}) 

    # remover coluna "ID" do DataFrame df
    df = df.drop(columns=["ID"])

    return df

def inserir_flex_br(df):
    """
    Função para inserir os dados do Flex BR no banco de dados.
    """
    # Lógica para inserir os dados do DataFrame df no banco de dados
    # Exemplo: df.to_sql('nome_da_tabela', con=engine, if_exists='replace', index=False)
    dados = df.to_dict(orient='records')

    engine = get_db_connection()

    with engine.connect() as connection:
        connection.execute(text(
                """
                INSERT INTO "flex_br" (ano, sexo, flex_br_rep, flex_br_nota)
                VALUES (:ano, :sexo, :flex_br_rep, :flex_br_nota)
                """),
            dados
        )
                
        connection.commit()  # Confirma a transação após cada inserção
    pass

df = importar_flex_br()

inserir_flex_br(df)

#print(importar_flex_br())


