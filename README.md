# 🚀 Motor de Preços 2.0 — SQL Edition (`motor-de-precos-2-sql`)

O **Motor de Preços 2.0 (SQL Edition)** é uma API REST e aplicação web para gestão, cálculo assíncrono e análise estatística de precificação dinâmica no e-commerce.

A aplicação foi reestruturada sob os princípios de **Clean Architecture** e alimentada por um banco de dados relacional assíncrono (**SQLAlchemy 2.0 + Asyncpg/Aiosqlite**), mantendo suporte completo à gestão via banco SQL, ingestão/exportação em lotes (`.xlsx` e `.docx`) e interface web dinâmica.

---

## 🎯 Destaques Técnicos & Arquitetura

* **Precisão Financeira Estrita:** Motor monetário baseado na classe `Decimal` (`ROUND_HALF_UP`), eliminando dízimas e imprecisões de arredondamento do tipo `float`.
* **Filtro Estatístico IQR:** Purga automática de preços anômalos (*outliers*) da concorrência através do algoritmo de Amplitude Interquartil (IQR) antes de calcular o valor ideal de mercado.
* **Persistência Assíncrona SQL:** Modelagem ORM desacoplada em SQLAlchemy 2.0 com suporte nativo a PostgreSQL (`asyncpg`) e SQLite assíncrono (`aiosqlite`).
* **Migrações Automatizadas (Alembic):** Controle de versão do esquema da base de dados através de scripts em `alembic/versions/`.
* **Exportação Executiva & Relatórios:** Geração dinâmica de relatórios em Word (`.docx`) e planilhas calculadas (`.xlsx`).
* **Qualidade & CI/CD:** Suíte de testes automatizados com `pytest` (cobertura unitária e de integração), ganchos Git (`pre-commit` e `pre-push`) e pipeline no GitHub Actions.
* **Compliance LGPD:** Arquitetura orientada a *Privacy by Design*, operando exclusivamente sobre dados de produtos, sem tráfego ou retenção de dados pessoais.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.10+, FastAPI, Uvicorn, Pydantic v2
* **ORM & Banco de Dados:** SQLAlchemy 2.0 (Async), Alembic, SQLite / PostgreSQL
* **Processamento de Dados & Documentos:** Pandas, OpenPyXL, Python-Docx
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
* **Testes & Qualidade:** Pytest, Pytest-Asyncio

---

## 🌐 Interface Web (Frontend)
A interface para testes interativos e envio de planilhas fica localizada no diretório frontend/. Ela comunica com os endpoints da API para submeter arquivos, consultar SKUs gravados no banco de dados e visualizar os cálculos de margem e precificação em tempo real.

## 📁 Estrutura do Projeto

```text
motor-de-precos-2-sql/
├── alembic/                # Scripts de migração de banco de dados
│   └── versions/           # Histórico de versões do esquema
├── app/
│   ├── api/                # Injeção de dependências e middlewares (deps.py)
│   ├── core/               # Configurações globais e segurança
│   ├── models/             # Modelos relacionais (SQLAlchemy) e domínio
│   ├── repositories/       # Camada de persistência (Base, SQL, Excel)
│   ├── routers/            # Endpoints REST da API
│   ├── schemas/            # Schemas de validação Pydantic
│   ├── services/           # Regras de negócio e motor de cálculo (IQR/Decimal)
│   ├── database.py         # Conexão e sessão assíncrona com o banco
│   └── main.py             # Instância FastAPI, estáticos e montagem das rotas
├── frontend/               # Interface web interativa
│   ├── static/             # Estilos CSS e scripts JS
│   └── templates/          # Templates HTML
├── scripts/                # Scripts utilitários e de carga de dados (Seed)
├── tests/                  # Suíte de testes unitários e de integração
├── .env.example            # Exemplo de variáveis de ambiente
├── alembic.ini             # Configuração do Alembic
├── pytest.ini              # Configuração do Pytest
└── requirements.txt        # Dependências do projeto
```
---

## ⚙️ Como Executar o Projeto
### 1. Clonar o Repositório e Criar o Ambiente Virtual
```Bash
git clone (https://github.com/cerqueirapg/motor-de-precos-2-sql.git)
cd motor-de-precos-2-sql
python -m venv .venv
# Ativar no Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Ativar no Linux/Mac:
source .venv/bin/activate
```
### 2. Instalar as Dependências
```Bash
pip install -r requirements.txt
```
### 3. Configurar Variáveis de Ambiente
Crie o arquivo .env na raiz do projeto copiando a estrutura do exemplo:
```Bash
cp .env.example .env
```
### 4. Executar as Migrações do Banco de Dados (Alembic)
Alique as migrações para criar a estrutura das tabelas relacionais:

```Bash
alembic upgrade head
```
### 5. Iniciar o Servidor de Desenvolvimento
```Bash
uvicorn app.main:app --reload
```
Acesse a aplicação no navegador em: http://127.0.0.1:8000

---

## 🔗 Endpoints da API
A documentação interativa OpenAPI (Swagger) está disponível em: http://127.0.0.1:8000/docs

* GET `/api/v1/health`: Verificação de integridade e estado da API.

* POST `/api/v1/pricing/calculate`: Recebe os dados de custo/concorrentes e calcula a precificação purgada via IQR.

* POST `/api/upload/excel`: Processa arquivos .xlsx em lote e grava/calcula margens.

* POST `/api/upload/export-docx`: Gera e faz o download do relatório executivo em Word (.docx).

* POST `/api/upload/export-xlsx`: Exporta a planilha consolidada com os preços recalculados.

---

## 🧪 Executando os Testes
Para rodar toda a suíte de testes unitários e de integração com banco de dados em memória:

```Bash
pytest -vv
```
## 📄 Licença e Créditos
Desenvolvido por Paulo Gonçalves Cerqueira como parte do ecossistema de soluções de engenharia de software e automação de precificação.