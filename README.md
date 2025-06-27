# API de Gerenciamento de Usuários

Esta é uma API simples para demonstração, construída com FastAPI, que gerencia usuários sem a necessidade de um banco de dados tradicional. Os dados são persistidos em um arquivo `users.json`.

## Como Executar

1.  **Crie um Ambiente Virtual (Recomendado):**
    ```bash
    python -m venv venv
    ```

2.  **Ative o Ambiente Virtual:**
    -   No Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    -   No macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Inicie o servidor:**
    ```bash
    uvicorn main:app --reload
    ```

A API estará disponível em `http://127.0.0.1:8000`.

A documentação interativa (Swagger UI) pode ser acessada em `http://127.0.0.1:8000/docs`.

---

## Endpoints da API

### 1. Criar um Novo Usuário

-   **Endpoint:** `POST /users`
-   **Descrição:** Cadastra um novo usuário no sistema.
-   **Corpo da Requisição (JSON):**
    ```json
    {
      "name": "string",
      "email": "user@example.com",
      "password": "string",
      "access_level": "read" 
    }
    ```
    -   `access_level` deve ser `"read"` ou `"write"`.
-   **Resposta de Sucesso (201 Created):**
    ```json
    {
      "name": "string",
      "email": "user@example.com",
      "access_level": "read",
      "is_active": true
    }
    ```
-   **Resposta de Erro (400 Bad Request):** Se o e-mail já estiver cadastrado.

### 2. Listar Todos os Usuários

-   **Endpoint:** `GET /users`
-   **Descrição:** Retorna uma lista com todos os usuários cadastrados.
-   **Resposta de Sucesso (200 OK):**
    ```json
    [
      {
        "name": "string",
        "email": "user@example.com",
        "access_level": "read",
        "is_active": true
      }
    ]
    ```

### 3. Autenticar Usuário

-   **Endpoint:** `POST /login`
-   **Descrição:** Autentica um usuário e retorna seus dados em caso de sucesso.
-   **Corpo da Requisição (JSON):**
    ```json
    {
      "email": "user@example.com",
      "password": "string"
    }
    ```
-   **Resposta de Sucesso (200 OK):**
    ```json
    {
      "name": "string",
      "email": "user@example.com",
      "access_level": "read"
    }
    ```
-   **Respostas de Erro:**
    -   `401 Unauthorized` ou `404 Not Found`: Credenciais inválidas.
    -   `403 Forbidden`: Usuário inativo.

### 4. Resetar a Senha do Usuário

-   **Endpoint:** `POST /users/{email}/reset-password`
-   **Descrição:** Reseta a senha de um usuário específico para `"teste123"`.
-   **Parâmetro de URL:**
    -   `email`: O e-mail do usuário a ter a senha resetada.
-   **Resposta de Sucesso (200 OK):** Retorna os dados do usuário com a senha atualizada.
-   **Resposta de Erro (404 Not Found):** Se o usuário com o e-mail especificado não for encontrado.

### 5. Desativar um Usuário

-   **Endpoint:** `DELETE /users/{email}`
-   **Descrição:** Inativa um usuário, mudando seu status `is_active` para `false`.
-   **Parâmetro de URL:**
    -   `email`: O e-mail do usuário a ser desativado.
-   **Resposta de Sucesso (200 OK):** Retorna os dados do usuário com o status atualizado.
-   **Resposta de Erro (404 Not Found):** Se o usuário com o e-mail especificado não for encontrado.

### 6. Reativar um Usuário

-   **Endpoint:** `POST /users/{email}/reactivate`
-   **Descrição:** Reativa um usuário previamente inativado, mudando seu status `is_active` para `true`.
-   **Parâmetro de URL:**
    -   `email`: O e-mail do usuário a ser reativado.
-   **Resposta de Sucesso (200 OK):** Retorna os dados do usuário com o status atualizado.
-   **Resposta de Erro (404 Not Found):** Se o usuário com o e-mail especificado não for encontrado.
