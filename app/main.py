from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.messages import router as messages_router
from app.db.db import Base, engine
from app.core.errors import api_error_handler, generic_error_handler, APIError
# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

# Registrar manejadores de error
app.add_exception_handler(APIError, api_error_handler)
app.add_exception_handler(Exception, generic_error_handler)

# Rutas
app.include_router(health_router, prefix="/api")
app.include_router(messages_router, prefix="/api")

@app.get("/", tags=["root"])
def root():
    return {"message": "Api para Chat de mensajes ingresar a /docs para su interacción"}
