
# API simple de procesamiento de mensajes

API RESTful para procesamiento de mensajes de chat, construida con **FastAPI**, **SQLite** y **SQLAlchemy**.  
Incluye validación, filtrado de contenido, metadatos automáticos, paginación, manejo robusto de errores y pruebas con **Pytest**.  

---

## Requisitos
- Python **3.10+**
- [pip](https://pip.pypa.io/en/stable/installation/)
- Opcional  [Docker](https://www.docker.com/) y [docker-compose](https://docs.docker.com/compose/)

---

## Instalación manual

# bash
# 1. Clonar repositorio
git clone https://github.com/tu_usuario/chat-message-api.git
cd chat-message-api

# 2. Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Copiar archivo de configuración
cp .env.example .env


---

##  Ejecución

# bash
ejecutar el comando 
uvicorn app.main:app --reload


La API estará disponible en:  
**http://127.0.0.1:8000**

Documentación interactiva:  
- Swagger UI: **http://127.0.0.1:8000/docs**  
- ReDoc: **http://127.0.0.1:8000/redoc**

---

## Endpoints principales

###  Healthcheck
'GET /api/health'  
Verifica que el servicio está arriba.  
# json
{ "status": "ok" }

---

###  Crear mensaje
'POST /api/messages'  
Recibe, valida, procesa y almacena un mensaje.  

#### Ejemplo de request json
{
  "message_id": "msg-123456",
  "session_id": "session-abcdef",
  "content": "Hola, ¿cómo puedo ayudarte hoy?",
  "timestamp": "2023-06-15T14:30:00Z",
  "sender": "system"
}


#### Ejemplo de respuesta json
{
  "message_id": "msg-123456",
  "session_id": "session-abcdef",
  "content": "Hola, ¿cómo puedo ayudarte hoy?",
  "timestamp": "2023-06-15T14:30:00Z",
  "sender": "system",
  "metadata": {
    "word_count": 6,
    "character_count": 32,
    "processed_at": "2023-06-15T14:30:01.123456"
  }
}

---

###  Recuperar mensajes
'GET /api/messages/{session_id}'  
Devuelve mensajes de una sesión, con **paginación** y **filtro por remitente**.  

#### Parámetros
- 'limit' (int, default=10, max=100) → cantidad de mensajes
- 'offset' (int, default=0) → desplazamiento para paginación
- 'sender' ('user' | 'system', opcional) → filtrar por remitente

#### Ejemplo

GET /api/messages/session-abcdef?limit=5&sender=user


---

###  Manejo de errores
Todos los errores siguen un formato estándar:

#### Ejemplo (sender inválido) json
{
  "status": "error",
  "error": {
    "code": "INVALID_FORMAT",
    "message": "Formato de mensaje inválido",
    "details": "El campo 'sender' debe ser 'user' o 'system'"
  }
}

---

##  Pruebas
Ejecutar todas las pruebas: 
# bash
pytest -v

Ejecutar con cobertura:
# bash
pytest --cov=app tests/

---

##  Despliegue con Docker

### 1. Construir imagen
# bash
docker build -t chat-message-api .

### 2. Ejecutar contenedor
# bash
docker run -d -p 8000:8000 chat-message-api


### 3. Con docker-compose
# bash
docker-compose up --build -d


La API quedará disponible en  **http://127.0.0.1:8000/docs**

---

##  Estructura del proyecto

chat-message-api/
│── app/
│   ├── api/v1/routes/   # Endpoints
│   ├── core/            # Configuración y manejo de errores
│   ├── db/              # Base de datos (SQLAlchemy)
│   ├── models/          # Modelos ORM
│   ├── schemas/         # Esquemas Pydantic
│   ├── services/        # Lógica de negocio
│   └── main.py          # App principal
│
│── tests/               # Pruebas unitarias e integración
│   ├── conftest.py
│   ├── test_health.py
│   └── test_messages.py
│
│── requirements.txt
│── README.md
│── .env.example
│── Dockerfile
│── docker-compose.yml
```

---


