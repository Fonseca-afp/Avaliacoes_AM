import pandas as pd
from bd_connection import get_db_connection
from sqlalchemy import text

sep=";"
decimal=","

def importar_alunos():
    """
    Função para importar os dados dos alunos.
    """
    # Lógica para importar os dados dos alunos e armazenar no DataFrame df
    
    # ler ficheiro csv com separador e decimal especificados
    df = pd.read_csv('/home/andre/projetos/Avaliacoes_AM/Avaliacoes_AM/dados/Alunos.csv', sep=sep, decimal=decimal) 

    # renomear colunas do DataFrame df
    df = df.rename(columns={"NIM": "nim", "Cod_Aluno": "cod_aluno", "Num_Corpo":"num_corpo", "Sexo":"sexo", "Ano":"ano", "Comp":"comp", "Posto":"posto",
                            "Nome": "nome", "Ramo": "ramo", "Curso": "curso", "Data_Nascimento": "data_nascimento", "Altura": "altura", "Peso": "peso"})

    df = df.astype(object).where(pd.notnull(df), None)
    return df

def inserir_alunos(df):
    """
    Função para inserir os dados dos alunos no banco de dados.
    """
    dados = df.to_dict(orient='records')
    

    engine = get_db_connection()
    if engine is None:
        raise RuntimeError("Falha ao conectar ao banco de dados.")

    with engine.connect() as connection:
        connection.execute(text(
                """
                INSERT INTO "Aluno" (nim, cod_aluno, num_corpo, sexo, ano, comp, posto, nome, ramo, curso, data_nascimento, altura, peso)
                VALUES (:nim, :cod_aluno, :num_corpo, :sexo, :ano, :comp, :posto, :nome, :ramo, :curso, :data_nascimento, :altura, :peso)
                """),
            dados
        )
                
        connection.commit()  # Confirma a transação após cada inserção
    pass

df = importar_alunos()

inserir_alunos(df)
