# 🚀 Motor de Preços 2.0

O **Motor de Preços 2.0** é uma API e aplicação web para gestão e cálculo assíncrono de precificação dinâmica com base em margens de segurança e análise de preços da concorrência.

A aplicação permite processar planilhas Excel (`.xlsx`), armazenar produtos em banco de dados relacional (PostgreSQL / SQLite via SQLAlchemy) e gerar relatórios executivos em formatos **DOCX** e **XLSX**.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.14+, FastAPI, Uvicorn
* **ORM & Banco de Dados:** SQLAlchemy, Alembic, SQLite / PostgreSQL
* **Processamento de Dados:** Pandas, OpenPyXL, Python-Docx
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API / AsRoad)
* **Testes:** Pytest

---

## 🌐 Frontend
A interface web para testes interativos e manipulação de uploads fica localizada no diretório `frontend/`. Ela comunica-se diretamente com os endpoints da API para enviar planilhas Excel e visualizar cálculos de preços em tempo real.

---

## 📁 Estrutura do Projeto

```text
motor-de-precos-2-sql/
├── app/
│   ├── core/               # Configurações globais e segurança
│   ├── models/             # Modelos de banco de dados (SQLAlchemy) e domínio
│   ├── repositories/       # Camada de acesso a dados (CRUD)
│   ├── routers/            # Endpoints da API (Upload, Precificação, etc.)
│   ├── schemas/            # Schemas de validação Pydantic
│   ├── services/           # Regras de negócio e motor de cálculo
│   ├── database.py         # Conexão e sessão do banco de dados
│   └── main.py             # Instância do FastAPI, montagem de estáticos e rotas
├── frontend/
│   ├── static/             # Estilos CSS e rotinas JavaScript
│   │   ├── styles.css
│   │   └── script.js
│   └── templates/          # Templates HTML (Jinja2)
│       └── index.html
├── scripts/                # Scripts utilitários e de carga de dados (Seed)
├── tests/                  # Testes unitários e de integração
├── alembic.ini             # Configurações de migração de banco
├── pytest.ini              # Configurações do Pytest
└── requirements.txt        # Dependências do projeto
```
---

## ⚙️ Como Executar o Projeto
### 1. Clonar o Repositório e Criar o Ambiente Virtual
```Bash
git clone <url-do-repositorio>
cd motor-de-precos-2-sql

# Criar ambiente virtual
python -m venv venv

# Ativar no Windows (PowerShell)
.\venv\Scripts\Activate.ps1
```
### 2. Instalar as Dependências
```Bash
pip install -r requirements.txt
```
### 3. Executar o Servidor de Desenvolvimento
```Bash
uvicorn app.main:app --reload
```
Acesse a aplicação no navegador em: http://127.0.0.1:8000

## 🔗 Endpoints da API
A documentação interativa OpenAPI (Swagger) fica disponível em: http://127.0.0.1:8000/docs

* POST `/api/upload/excel`: Recebe a planilha de preços e retorna o cálculo de margens e sugestão de valores.

* POST `/api/upload/export-docx`: Exporta o relatório comparativo formatado em Word (.docx).

* POST `/api/upload/export-xlsx`: Exporta a planilha consolidada de precificação (.xlsx).

## 🧪 Executando os Testes
Para rodar a suíte de testes automatizados com o pytest:
```Bash
pytest
```
