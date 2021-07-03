from fastapi                    import Depends, FastAPI
from fastapi.middleware.cors    import CORSMiddleware

from routers.users_router       import router as router_users

api = FastAPI()
origins = [
    "http://localhost", "http://localhost:8080"
]

api.add_middleware(
    CORSMiddleware, allow_origins=origins,
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@api.get("/")
async def hello():
    return "Bienvenidos a Connek. Esta es una prueba de conexión"

api.include_router(router_users)