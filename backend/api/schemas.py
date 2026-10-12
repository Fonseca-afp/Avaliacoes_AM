from pydantic import BaseModel, Field, model_validator
from datetime import date, time

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

"""class TFBCreate(BaseModel):
    nim: str
    tipo_aval: str;
    flex_br_rep: int |None = None
    flex_br_nota: float |None = None
    abd_rep: int |None = None
    abd_nota: float| None = None
    bola_dist: int |None = None
    bola_nota: float | None = None
    salto_dist: int |None = None
    salto_nota: float |None = None
    cooper_dist: int |None = None
    cooper_nota: float | None = None"""

class TFBUpdate(BaseModel):
    flex_br_rep: int | None = None
    abd_rep: int | None = None
    bola_dist: int | None = None
    salto_dist: int | None = None
    voltas: int | None = None
    metros: int | None = None
    pista: str | None = None

class TFAMUpdate(BaseModel):
    tempo_inicio: time | None = None
    tempo_fim: time | None = None
    acertos: time | None = None
    granadas_menos_5m: int | None = Field(default= None, ge=0, le=4)
    granadas_5m: int | None = Field(default= None, ge=0, le=4)
    granadas_10m: int | None = Field(default= None, ge=0, le=4)
    granadas_15m: int | None = Field(default= None, ge=0, le=4)
    apoios: int | None = None
    marfor_no_tempo: bool | None = None
    @model_validator(mode="after")
    def validar_granadas(self):
        granadas_menos_5m = self.granadas_menos_5m or 0
        granadas_5m = self.granadas_5m or 0
        granadas_10m = self.granadas_10m or 0
        granadas_15m = self.granadas_15m or 0

        total_granadas = granadas_menos_5m + granadas_5m + granadas_10m + granadas_15m

        if total_granadas > 4:
            raise ValueError("O total de granadas não pode exceder 4.")

        return self

class ModalidadeResultadoUpdate(BaseModel):
    nota: float = Field(ge=0, le=20)

class ACEUpdate(BaseModel):
    ace: str | None = None
    funcao: str | None = None
    tipo_prova: str | None = None