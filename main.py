from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Request
from pydantic import BaseModel
import pandas as pd
import os
from typing import List
from datetime import datetime
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import glob

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

@app.post("/upload-logo")
async def upload_logo(file: UploadFile = File(...)):
    # Verifica se o arquivo é uma imagem
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        raise HTTPException(status_code=400, detail="Arquivo deve ser uma imagem (PNG, JPG, JPEG ou GIF)")
    
    # Cria um nome único para o arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = Path(file.filename).suffix
    file_name = f"uploads/logo/logo_{timestamp}{file_extension}"
    
    try:
        # Salva o arquivo
        contents = await file.read()
        with open(file_name, 'wb') as f:
            f.write(contents)
        
        return {
            "message": "Logo enviada com sucesso",
            "filename": file_name
        }
    except Exception as e:
        if os.path.exists(file_name):
            os.remove(file_name)
        raise HTTPException(status_code=500, detail=f"Erro ao salvar logo: {str(e)}")

@app.post("/upload-images")
async def upload_images(files: List[UploadFile] = File(...)):
    if len(files) == 0:
        raise HTTPException(status_code=400, detail="Nenhum arquivo enviado")
    
    saved_files = []
    for file in files:
        # Verifica se o arquivo é uma imagem
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            continue
        
        # Cria um nome único para o arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = Path(file.filename).suffix
        file_name = f"uploads/images/image_{timestamp}_{len(saved_files)}{file_extension}"
        
        try:
            # Salva o arquivo
            contents = await file.read()
            with open(file_name, 'wb') as f:
                f.write(contents)
            
            saved_files.append(file_name)
        except Exception as e:
            if os.path.exists(file_name):
                os.remove(file_name)
            continue
    
    if not saved_files:
        raise HTTPException(status_code=400, detail="Nenhuma imagem válida foi enviada")
    
    return {
        "message": f"{len(saved_files)} imagens enviadas com sucesso",
        "files": saved_files
    }

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    # Verifica se o arquivo é uma imagem
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        raise HTTPException(status_code=400, detail="Arquivo deve ser uma imagem (PNG, JPG, JPEG ou GIF)")
    
    # Cria um nome único para o arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = Path(file.filename).suffix
    file_name = f"uploads/images/image_{timestamp}{file_extension}"
    
    try:
        # Salva o arquivo
        contents = await file.read()
        with open(file_name, 'wb') as f:
            f.write(contents)
        
        return {
            "message": "Imagem enviada com sucesso",
            "file": file_name
        }
    except Exception as e:
        if os.path.exists(file_name):
            os.remove(file_name)
        raise HTTPException(status_code=500, detail=f"Erro ao salvar imagem: {str(e)}")

@app.post("/gerar-template-menu")
async def gerar_template_menu():
    try:
        # Dimensões do template
        width = 800
        height = 1200
        header_height = 200
        
        # Encontrar todos os logos
        logos = glob.glob("uploads/logo/*")
        if not logos:
            raise HTTPException(status_code=404, detail="Nenhum logo encontrado")
            
        templates_gerados = []
        
        for i, logo_path in enumerate(logos[:3], 1):
            # Criar template base
            template = Image.new('RGB', (width, height), color='#2B3A2B')  # Verde escuro
            
            # Carregar e redimensionar logo
            logo = Image.open(logo_path)
            # Manter proporção
            logo_ratio = min(header_height/logo.height, (width-40)/logo.width)
            new_size = (int(logo.width * logo_ratio), int(logo.height * logo_ratio))
            logo = logo.resize(new_size, Image.Resampling.LANCZOS)
            
            # Posicionar logo no centro do cabeçalho
            logo_position = ((width - logo.width) // 2, (header_height - logo.height) // 2)
            template.paste(logo, logo_position, logo if logo.mode == 'RGBA' else None)
            
            # Adicionar borda decorativa
            draw = ImageDraw.Draw(template)
            draw.rectangle([(20, 20), (width-20, height-20)], outline='#8B7355', width=2)
            
            # Salvar template
            template_path = f"uploads/templates/menu_template_{i}.png"
            os.makedirs("uploads/templates", exist_ok=True)
            template.save(template_path, "PNG")
            templates_gerados.append(template_path)
            
        return {
            "message": f"{len(templates_gerados)} templates gerados com sucesso",
            "templates": templates_gerados
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar templates: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 