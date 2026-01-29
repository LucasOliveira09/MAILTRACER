import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# Certifique-se de que o arquivo analising.py está na mesma pasta
from analising import classificar_email 

app = FastAPI()

# Configuração de CORS (Essencial para o front-end acessar)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, idealmente troque "*" pelo URL do seu site
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
        # Chama sua função de IA
        categoria, resposta = classificar_email(dados.texto)

        return {
            "categoria": categoria,
            "resposta": resposta
        }

    except Exception as e:
        print(f"Erro no servidor: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# Bloco para rodar localmente ou via comando python direto
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)