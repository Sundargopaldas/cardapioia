import pandas as pd

# Dados do cardápio
dados = {
    'nome': [
        'X-Tudo',
        'Coca-Cola 350ml',
        'Batata Frita',
        'Pizza Margherita',
        'Pudim'
    ],
    'descricao': [
        'Hambúrguer com tudo dentro',
        'Refrigerante Coca-Cola Lata',
        'Porção de batata frita crocante',
        'Pizza com molho de tomate, mozzarella e manjericão',
        'Pudim de leite condensado tradicional'
    ],
    'preco': [25.90, 5.90, 15.90, 45.90, 12.90],
    'categoria': [
        'Lanches',
        'Bebidas',
        'Porções',
        'Pizzas',
        'Sobremesas'
    ]
}

# Criar DataFrame
df = pd.DataFrame(dados)

# Salvar como Excel
df.to_excel('cardapio_exemplo.xlsx', index=False)
print("Arquivo cardapio_exemplo.xlsx criado com sucesso!") 