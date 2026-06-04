from fastapi import FastAPI, Request 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.controllers import auth, post
from src.exceptions import NotFoundPostError

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
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, tags=["auth"])
app.include_router(post.router, tags=["Posts"])


@app.exception_handler(NotFoundPostError)
async def not_found_post_exception_handler(request: Request, exc: NotFoundPostError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )



