# Trabalho_Final_POO
Trabalho final Realizado em conjunto com os membros: Carlos Amorin, Cauan Riffel e Giovani Pott


# Sistema de Gestão de Estoque e Processamento de Vendas — Arquitetura Orientada a Objetos

Este repositório apresenta a implementação de um sistema modular para controle de estoque, gerenciamento de carrinho de compras e fluxo de venda, estruturado segundo os princípios da Programação Orientada a Objetos (POO) em Python. O projeto adota boas práticas de organização de código, encapsulamento, abstração e segregação de responsabilidades.

## Arquitetura do Sistema

O sistema é composto por módulos independentes localizados em `models/`, onde cada classe representa uma entidade funcional do domínio de vendas e operações internas.

### Produto
Define a entidade básica do sistema. Armazena atributos essenciais como:
- Identificador único
- Nome e marca
- Preço unitário
- Função e tipo categórico  
Serve como unidade fundamental nas operações de estoque, carrinho e venda.

### Estoque
Responsável pelo gerenciamento centralizado dos produtos disponíveis. As principais funções incluem:
- Registro e remoção de itens
- Controle de quantidade
- Organização da lista de produtos  
É o módulo que representa a fonte oficial de itens para operações de compra.

### Carrinho
Controla os itens selecionados pelo usuário ao longo do fluxo de compra. Suas funcionalidades principais incluem:
- Armazenamento de produtos
- Cálculo da quantidade total
- Limpeza e redefinição dos itens registrados  
Atua como estrutura intermediária entre o estoque e a finalização da compra.

### Fornecedor
Representa entidades externas responsáveis pelo suprimento de produtos. Permite:
- Registro de itens fornecidos
- Integração com o estoque interno  
Garante a composição da cadeia de suprimentos simulada no sistema.

### Usuário e Funcionário
Modelam entidades humanas que interagem com o sistema:
- Usuário: cliente final, com atributos de identificação e histórico de compra.
- Funcionário: especialização do usuário, com permissões e ações administrativas.  
Aplicam princípios de herança e extensão de comportamento.

### Caixa
Responsável por mediar o processo de atendimento e finalização de compra. Representa a interação operacional entre funcionário, carrinho e métodos de pagamento.

### Pagamento
Classe destinada à modelagem das operações de quitação da compra. Atualmente com funções abstratas, permitindo extensões como:
- Pagamento em cartão
- Pagamento digital
- Processamento via gateways externos

## Estrutura do Repositório

```txt
Trabalho_Final_POO/
├── models/
│   ├── caixa.py
│   ├── carrinho.py
│   ├── estoque.py
│   ├── fornecedor.py
│   ├── pagamento.py
│   ├── produto.py
│   ├── usuario.py
│   └── __init__.py
└── README.md

```
## Considerações Técnicas

- O projeto segue uma abordagem modular, com cada classe isolada em seu próprio arquivo.
- A arquitetura é adequada para expansão em direção a um sistema completo de vendas.
- Alguns métodos permanecem deliberadamente não implementados, permitindo personalização conforme as necessidades:
  - Gateways de pagamento
  - Regras de negócio para descontos e validações
  - Integração real com interfaces gráficas ou APIs

O sistema é apropriado para fins acadêmicos, testes de modelagem orientada a objetos e prototipagem de funcionalidades em aplicações de venda e controle interno.