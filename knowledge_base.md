# Base de Conhecimento para Automação de AMS

## 1. Visão Geral do Sistema

Este documento serve como base de conhecimento para um sistema de automação de Application Management Services (AMS) gerenciado por Inteligência Artificial (IA). O sistema em questão é uma aplicação web para gerenciamento de usuários, com front-end desenvolvido em HTML, CSS e JavaScript, e back-end em Python utilizando o framework FastAPI.

A aplicação permite o cadastro, autenticação e gerenciamento de usuários, que são armazenados em um arquivo `users.json`. Os usuários podem ter dois níveis de acesso: "leitura" (read) e "escrita" (write).

## 2. Arquitetura e Tecnologias

- **Front-end:** HTML, CSS, JavaScript
- **Back-end:** Python, FastAPI
- **Banco de Dados:** Arquivo JSON (`users.json`)
- **Dependências Python:** `fastapi`, `uvicorn`, `bcrypt`, `pydantic`, `email-validator`

## 3. Autenticação

Todas as chamadas para a API, exceto para o endpoint de login, devem incluir um header de autenticação `X-API-Key` com a chave de API configurada na variável de ambiente `API_KEY`.

## 4. Endpoints da API

A seguir estão os endpoints da API disponíveis para interação com o sistema:

- `POST /users`: Cria um novo usuário.
- `GET /users`: Retorna uma lista de todos os usuários.
- `POST /login`: Autentica um usuário.
- `POST /users/{email}/reset-password`: Reseta a senha de um usuário para "teste123".
- `DELETE /users/{email}`: Desativa um usuário.
- `POST /users/{email}/reactivate`: Reativa um usuário.
- `PUT /users/{email}/access-level`: Atualiza o nível de acesso de um usuário.

## 5. Operações Permitidas para a IA

A IA tem permissão para realizar as seguintes operações de forma autônoma:

### 5.1. Criação de Usuário com Acesso de Leitura

- **Descrição:** Criar um novo usuário no sistema com nível de acesso de "leitura".
- **Endpoint a ser utilizado:** `POST /users`
- **Header Obrigatório:** `X-API-Key`
- **Payload Exemplo:**
  ```json
  {
    "name": "Nome do Usuário",
    "email": "usuario@exemplo.com",
    "password": "senha_temporaria",
    "access_level": "read"
  }
  ```
- **Observação:** A senha inicial pode ser uma string aleatória ou um valor padrão que o usuário será instruído a alterar no primeiro acesso.

### 5.2. Reset de Senha de Usuários

- **Descrição:** Resetar a senha de um usuário existente para um valor padrão.
- **Endpoint a ser utilizado:** `POST /users/{email}/reset-password`
- **Header Obrigatório:** `X-API-Key`
- **Parâmetro na URL:** `email` do usuário.
- **Observação:** O endpoint atualmente reseta a senha para "teste123".

### 5.3. Gerenciamento de Níveis de Acesso

- **Descrição:** Atualizar o nível de acesso de um usuário existente.
- **Endpoint a ser utilizado:** `PUT /users/{email}/access-level`
- **Header Obrigatório:** `X-API-Key`
- **Parâmetro na URL:** `email` do usuário.
- **Payload Exemplo:**
  ```json
  {
    "access_level": "write"
  }
  ```
