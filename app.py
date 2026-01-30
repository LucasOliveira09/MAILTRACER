import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from analising import classificar_email 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mailtracer.vercel.app"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailRequest(BaseModel):
    texto: str

@app.post("/analisar")
def analisar(dados: EmailRequest):
    if not dados.texto.strip():
        raise HTTPException(status_code=400, detail="O texto está vazio.")

    try:
        categoria, resumo, resposta = classificar_email(dados.texto)

        return {
            "categoria": categoria,
            "resumo": resumo,
            "resposta": resposta
        }

    except Exception as e:
        print(f"Erro no servidor: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)