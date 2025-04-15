from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pandas as pd
import os
from typing import List
from datetime import datetime

app = FastAPI()

class Credentials(BaseModel):
    user: str
    password: str

class MenuItem(BaseModel):
    nome: str
    descricao: str
    preco: float
    categoria: str

@app.post("/verify")
async def verify_credentials(credentials: Credentials):
    # Verifica se as credenciais correspondem aos valores esperados
    is_valid = credentials.user == "user" and credentials.password == "pass"
    return {"is_valid": is_valid}

@app.post("/upload-cardapio")
async def upload_cardapio(file: UploadFile = File(...)):
    # Verifica se o arquivo é um XLS/XLSX
    if not file.filename.endswith(('.xls', '.xlsx')):
        return {"error": "Arquivo deve ser XLS ou XLSX"}
    
    # Cria um nome único para o arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"uploads/cardapio_{timestamp}_{file.filename}"
    
    # Salva o arquivo
    try:
        contents = await file.read()
        with open(file_name, 'wb') as f:
            f.write(contents)
        
        # Lê o arquivo Excel
        df = pd.read_excel(file_name)
        
        # Converte para lista de dicionários
        items = []
        for _, row in df.iterrows():
            item = {
                "nome": str(row.get('nome', '')),
                "descricao": str(row.get('descricao', '')),
                "preco": float(row.get('preco', 0)),
                "categoria": str(row.get('categoria', ''))
            }
            items.append(item)
        
        return {
            "message": "Arquivo processado com sucesso",
            "filename": file_name,
            "items": items
        }
    
    except Exception as e:
        if os.path.exists(file_name):
            os.remove(file_name)
        return {"error": f"Erro ao processar arquivo: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 