import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

db_url = os.getenv("DATABASE_URL")

if db_url is None:
    raise RuntimeError("DATABASE_URL não definida.")

# Criado apenas uma vez quando o módulo é carregado
engine = create_engine(db_url)

def get_db_connection():
    """
    Devolve o engine SQLAlchemy já criado.
    """
    return engine


def test_connection():
    with engine.connect() as connection:
        result = connection.execute(
            text('SELECT * FROM "Aluno"')
        ).fetchall()

        return result

# print(test_connection())