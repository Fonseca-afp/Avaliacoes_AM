CREATE TYPE "Resultado" AS ENUM (
  'Aprovado',
  'Nao_Aprovado',
  'Exame',
  'IF'
);

CREATE TYPE "Ramo" AS ENUM (
  'EXE',
  'GNR'
);

CREATE TYPE "Curso" AS ENUM (
  'INF',
  'CAV',
  'ART',
  'ADMIL',
  'TM',
  'ENG',
  'SMAT_E',
  'SMAT_M',
  'ARMAS',
  'MED',
  'QETS'
);

CREATE TYPE "Funcao" AS ENUM (
  'delegado',
  'atleta'
);

CREATE TABLE "Aluno" (
  "nim" int PRIMARY KEY,
  "cod_aluno" int,
  "num_corpo" int UNIQUE NOT NULL,
  "ano" int,
  "nome" varchar(50),
  "ramo" "Ramo",
  "curso" "Curso",
  "sexo" varchar(1),
  "data_nascimento" date,
  "altura" float,
  "peso" float
);

CREATE TABLE "TFB" (
  "id" int PRIMARY KEY,
  "tipo_aval" varchar(10),
  "nim" int,
  "flex_br_rep" int,
  "ext_br_rep" int,
  "abd_rep" int,
  "cooper_dist" int,
  "flex_br_nota" int,
  "ext_br_nota" int,
  "abd_nota" int,
  "cooper_nota" int,
  "nota" float
);

CREATE TABLE "Modalidade" (
  "id" int PRIMARY KEY,
  "nome" varchar(20)
);

CREATE TABLE "ModalidadeResultado" (
  "id" int PRIMARY KEY,
  "nim" int,
  "modalidade_id" int,
  "tipo_aval" varchar(10),
  "nota" float
);

CREATE TABLE "TFB_Final" (
  "id" int PRIMARY KEY,
  "nim" int,
  "gin_nota" float,
  "nota_tfb" float,
  "tfb_final" float,
  "resultado" "Resultado"
);

CREATE TABLE "TFAM" (
  "id" int PRIMARY KEY,
  "nim" int,
  "tipo_prova" varchar(20),
  "tipo_aval" varchar(10),
  "tempo_inicio" interval,
  "tempo_fim" interval,
  "acertos" interval,
  "tempo_final" interval,
  "nota_base" float
);

CREATE TABLE "TFAM_Triatlo" (
  "id" int PRIMARY KEY,
  "tfam_id" int,
  "granadas_5m" int,
  "granadas_10m" int,
  "granadas_15m" int,
  "granadas_menos_5m" int,
  "apoios" int
);

CREATE TABLE "TFAM_Final" (
  "id" int PRIMARY KEY,
  "nim" int,
  "tfam_id" int,
  "nota_base" float,
  "tfam_final" float,
  "resultado" "Resultado"
);

CREATE TABLE "PesoGrII" (
  "id" int PRIMARY KEY,
  "ano" int,
  "componente" varchar(10),
  "peso" float
);

CREATE TABLE "ClassFinal" (
  "id" int PRIMARY KEY,
  "nim" int,
  "tfb_final" float,
  "tfam_final" float,
  "f311_nota" float,
  "tfb_exame" float,
  "tfb_exame_resultado" "Resultado",
  "tfam_exame" float,
  "tfam_exame_resultado" "Resultado",
  "class_final" float
);

CREATE TABLE "flex_br" (
  "id" int PRIMARY KEY,
  "sexo" varcahr(1),
  "flex_br_rep" int,
  "flex_br_nota" float
);

CREATE TABLE "ext_br" (
  "id" int PRIMARY KEY,
  "sexo" varcahr(1),
  "ext_br_rep" int,
  "ext_br_nota" float
);

CREATE TABLE "cooper" (
  "id" int PRIMARY KEY,
  "sexo" varcahr(1),
  "cooper_dist" int,
  "cooper_nota" float
);

CREATE TABLE "Pista200" (
  "id" int PRIMARY KEY,
  "sexo" varcahr(1),
  "tempo" interval,
  "nota" float
);

CREATE TABLE "Pista500" (
  "id" int PRIMARY KEY,
  "sexo" varcahr(1),
  "tempo" interval,
  "nota" float
);

CREATE TABLE "Marcor" (
  "id" int PRIMARY KEY,
  "sexo" varcahr(1),
  "tempo" interval,
  "nota" float
);

CREATE TABLE "PistaTriatlo" (
  "id" int PRIMARY KEY,
  "sexo" varcahr(1),
  "tempo" interval,
  "nota" float
);

CREATE TABLE "AnoModalidades" (
  "id" int PRIMARY KEY,
  "ano" int,
  "modalidade" varchar(20),
  "peso" float
);

CREATE TABLE "Lesoes" (
  "id" int PRIMARY KEY,
  "nim" int NOT NULL,
  "data_ocorrencia" date,
  "situacao" varchar(100),
  "lesao" varchar(200),
  "mecanismo_lesao" varchar(100),
  "zn_anatomica" varchar(100),
  "gravidade" varchar(50),
  "recuperacao" varchar(10),
  "tem_dispensa" boolean,
  "dispensa_dias" int,
  "obs" varchar(200),
  "data_atualizacao" timestamp
);

CREATE TABLE "ACE" (
  "id" int PRIMARY KEY,
  "nim" int,
  "tipo_prova" varchar(20),
  "ace" varchar(50),
  "funcao" "Funcao"
);

ALTER TABLE "TFB" ADD FOREIGN KEY ("nim") REFERENCES "Aluno" ("nim") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "ModalidadeResultado" ADD FOREIGN KEY ("nim") REFERENCES "Aluno" ("nim") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "ModalidadeResultado" ADD FOREIGN KEY ("modalidade_id") REFERENCES "Modalidade" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "TFB_Final" ADD FOREIGN KEY ("nim") REFERENCES "Aluno" ("nim") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "TFAM" ADD FOREIGN KEY ("nim") REFERENCES "Aluno" ("nim") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "TFAM_Triatlo" ADD FOREIGN KEY ("tfam_id") REFERENCES "TFAM" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "TFAM_Final" ADD FOREIGN KEY ("nim") REFERENCES "Aluno" ("nim") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "TFAM_Final" ADD FOREIGN KEY ("tfam_id") REFERENCES "TFAM" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "ClassFinal" ADD FOREIGN KEY ("nim") REFERENCES "Aluno" ("nim") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "Lesoes" ADD FOREIGN KEY ("nim") REFERENCES "Aluno" ("nim") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "ACE" ADD FOREIGN KEY ("nim") REFERENCES "Aluno" ("nim") DEFERRABLE INITIALLY IMMEDIATE;
