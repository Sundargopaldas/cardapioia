# API de Verificação de Credenciais

Esta é uma API simples que verifica credenciais de usuário.

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Executando a API

Execute o seguinte comando:
```bash
python main.py
```

A API estará disponível em `http://localhost:8000`

## Uso

Envie uma requisição POST para `/verify` com o seguinte formato JSON:

```json
{
    "user": "user",
    "password": "pass"
}
```

A API retornará um JSON com um campo `is_valid` que será `true` se as credenciais estiverem corretas e `false` caso contrário.

## Documentação

Você pode acessar a documentação da API em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc` 