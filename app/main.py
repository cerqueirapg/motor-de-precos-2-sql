import os
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.db_models import Product
from app.routers import pricing, upload

# 1. Instância Única da Aplicação
app = FastAPI(
    title="Motor de Preços 2.0",
    description="Engine de precificação inteligente baseada em dados de concorrentes e margens de segurança.",
    version="2.0.0",
)

# 2. Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Inclusão dos Routers de API
app.include_router(pricing.router)
app.include_router(upload.router)

# 4. Configuração do Frontend e Arquivos Estáticos
frontend_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend")
)

# Servir arquivos estáticos (CSS, JS) da pasta frontend/
static_path = os.path.join(frontend_path, "static")

# Monta a rota /static apontando diretamente para frontend/static
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

# Configuração do motor de templates Jinja2 (procura dentro de frontend/)
templates = Jinja2Templates(directory=os.path.join(frontend_path, "templates"))


# 5. Rota Principal do Dashboard (Jinja2)
@app.get("/", tags=["Frontend"])
async def render_dashboard(
    request: Request, db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(Product))
    products = result.scalars().all()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "products": products},
    )
