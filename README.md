# 🏅 Sistema de Análise de Medalhas Olímpicas e Login

Este projeto consiste em uma aplicação interativa desenvolvida em Python com interface gráfica, voltada para consulta, análise e gerenciamento de dados sobre medalhas olímpicas, além de um sistema de login e cadastro de usuários.

## 📌 Funcionalidades

### 🔐 Módulo de Login e Cadastro
- Cadastro de usuários com validações de:
  - Nome de usuário
  - Email
  - Telefone com DDI e DDD (ex: +5581999999999)
  - Senha (letra maiúscula, minúscula e caractere especial)
- Login com autenticação por nome de usuário ou telefone
- Redefinição de senha
- Armazenamento seguro usando *SQLite*

### 📊 Módulo de Medalhas Olímpicas
- Consulta dinâmica com perguntas
  - Exemplos:  
    - “Histórico de medalhas do Brasil”  
    - “Top 15 países com mais medalhas de ouro”  
    - “Países sem medalha de bronze”
- Exibição dos dados em tabela
- Gerenciamento completo dos dados diretamente no arquivo .xlsx (CRUD) 
  - Adicionar novo registro
  - Editar registro existente
  - Remover registros

## 🛠 Tecnologias Utilizadas

- *Python 3*
- *CustomTkinter* – Interface moderna e customizável
- *Tkinter (messagebox, ttk)* – Componentes básicos e mensagens
- *Pandas* – Manipulação de dados
- *SQLite3* – Banco de dados local para usuários
- *Hashlib* – Criptografia de senhas
- *RE* – Validação de entradas
- *Difflib (SequenceMatcher)* – Similaridade textual para reconhecer os países
- *Visual Studio Code* – Editor de código
- *GitHub* – Plataforma de hospedagem do código 

## 🚀 Como Executar o Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/JunioSantos005/medalhas_olimpicas
   cd medalhas_olimpicas