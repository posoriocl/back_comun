from fastapi import FastAPI, HTTPException
from connect import connect
from config import load_config
from rutas.usuario import ruta

app = FastAPI()
app.include_router(ruta)


# connect to bbdd
config = load_config ('app_config.ini', 'postgresql')
cnn= connect(config)

@app.get('/')
def mensaje():
    return "Hola Juanny"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)