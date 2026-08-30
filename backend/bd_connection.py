import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
db_url = os.getenv("DATABASE_URL")

def get_db_connection():
    """
    Establishes a connection to the database using SQLAlchemy.

    Returns:
        engine: SQLAlchemy engine object for database connection.
    """
    try:
        engine = create_engine(db_url)
        return engine
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def test_connection():
    engine = get_db_connection()
    if engine is None:
        print("Failed to connect to the database.")
        return None
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM \"Aluno\"")).fetchall()
        return result

print(test_connection())