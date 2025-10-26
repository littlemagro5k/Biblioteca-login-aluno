# Biblioteca Escolar — Guia de Execução

Este projeto reúne o backend em Flask/SQLite e o frontend em React (Vite) para uma biblioteca escolar. As instruções abaixo explicam como preparar o ambiente, criar o banco de dados e abrir o site no Google Chrome.

## 1. Pré-requisitos
- Python 3.10 ou superior
- Node.js 18 ou superior (com `npm`)

## 2. Configurar o backend
1. (Opcional) Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .\.venv\Scripts\activate
   ```
2. Instale as dependências do Flask:
   ```bash
   pip install -r requirements.txt
   ```
3. Gere o banco de dados inicial (caso queira popular manualmente):
   ```bash
   python backend/init_db.py
   ```
4. Suba a API Flask:
   ```bash
   python backend/app.py
   ```
   > Se o arquivo `biblioteca.db` não existir, ele será criado automaticamente na primeira execução.

## 3. Configurar o frontend
1. Instale as dependências JavaScript:
   ```bash
   npm install
   ```
2. Ambiente de desenvolvimento (hot reload):
   ```bash
   npm run dev -- --host
   ```
   Acesse [http://localhost:5173](http://localhost:5173) no Chrome. O Vite encaminhará as chamadas à API Flask que estiver rodando em `http://localhost:5000`.
3. Build de produção:
   ```bash
   npm run build
   npm run preview
   ```
   O comando `npm run preview` serve o build pronto em `http://localhost:4173`.

## 4. Abrir no Google Chrome
- **Modo desenvolvimento:** `http://localhost:5173`
- **Build de produção (preview):** `http://localhost:4173`
- **Servido pelo Flask:** `http://localhost:5000`

Certifique-se de manter o backend rodando em um terminal e o frontend em outro para que todas as rotas funcionem corretamente.
