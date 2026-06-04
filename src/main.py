from contextlib import asynccontextmanager

from fastapi import FastAPI, Request        
from fastapi.responses import JSONResponse

from src.controllers import auth, post
from src.database import database, metadata, engine
from src.exceptions import NotFoundPostError



@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()
    
    
tags_metadata = [
    {
        "name": "auth",
        "description": "Operações para autenticação.",
    },
    {
        "name": "Post",
        "description": "Operações para manter posts.",
        "externalDocs": {
            "description": "Documentação externa para Posts.api",
            "url": "https://post-api.com/",
        },
    },
]


servers = [
    {"url": "http://localhost:8000", "description": "Servidor local"},
    {"url": "https://api.dio-blog.com", "description": "Servidor de produção"},
]   
    

app = FastAPI(
    title="Dio Blog API",
    version="1.2.0",
    summary="API para um blog pessoal",
    description="""API de um blog simples feita com FastAPI.
    ## Posts
    Você será capaz de fazer:
    * **Criar** posts** 
    * **Recuperar posts** 
    * **Recuperar posts po ID** 
    * **Atualizar posts** 
    * **Excluir posts**  
    * **Limitar quantidade de posts diários**
    """,
    openapi_tags=tags_metadata,
    servers=servers,
    redoc_url=None, 
    # openapi_url= None, # desabilita a documentação automática
    lifespan=lifespan,
)
app.include_router(auth.router, tags=["auth"])
app.include_router(post.router, tags=["Posts"])

@app.exception_handler(NotFoundPostError)
async def not_found_post_exception_handler(request: Request, exc: NotFoundPostError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )



