from pydantic import BaseModel
from datetime import date

class AlunoCreate(BaseModel):
    nim: str
    cod_aluno: int
    num_corpo: int
    ano: int
    comp: int
    posto:str
    nome: str
    ramo: str
    curso: str
    sexo: str
    data_nascimento: date
    altura: float | None= None
    peso: float | None= None


class AlunoUpdate(BaseModel):
    ano: int | None = None
    comp: int | None = None
    posto: str | None = None
    ramo: str | None = None
    curso: str | None = None
    altura: float | None = None
    peso: float | None = None

class TFBCreate(BaseModel):
    nim: str
    tipo_aval: str;
    flex_br_rep: int
    flex_br_nota: float |None = None
    abd_rep: int
    abd_nota: float| None = None
    bola_dist: int
    bola_nota: float | None = None
    salto_dist: int
    salto_nota: float |None = None
    cooper_dist: int
    cooper_nota: float | None = None

class TFBUpdate(BaseModel):
    flex_br_rep: int | None = None
    abd_rep: int | None = None
    bola_dist: int | None = None
    salto_dist: int | None = None
    cooper_dist: int | None = None
