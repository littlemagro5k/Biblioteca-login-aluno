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
   > Para ambientes hospedados (como a Vercel), defina a variável `VITE_API_URL` apontando para a URL pública da API Flask (ex.: `https://sua-api.exemplo.com`). As requisições do frontend utilizarão automaticamente esse endereço quando presente.

## 4. Deploy do backend no Render
1. Faça o push do repositório para o GitHub (ou outro provedor) contendo este projeto.
2. Com a conta criada no [Render](https://render.com), clique em **New + → Web Service** e conecte o repositório.
3. Quando o Render detectar o projeto, confirme as opções:
<<<<<<< ours
   - **Runtime**: Python (detectado automaticamente por causa do `requirements.txt`).
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn backend.app:app`
4. Em **Environment Variables**, defina:
=======
   - **Ambiente de execução (Runtime)**: Python (detectado automaticamente por causa do `requirements.txt`).
   - **Comando de build**: `pip install --root-user-action=ignore -r requirements.txt`
   - **Comando de inicialização**: `gunicorn backend.app:app`
4. Em **Environment Variables** (Variáveis de ambiente), defina:
>>>>>>> theirs
   - `FLASK_SECRET_KEY`: gere pelo botão *Generate* ou informe um valor próprio.
   - `DATABASE_PATH`: use `/var/data/biblioteca.db` para persistir o SQLite no disco.
   - `FRONTEND_ORIGIN`: informe a(s) origem(ns) autorizadas a consumir a API, separadas por vírgula. Ex.: `https://seu-site.vercel.app,http://localhost:5173`.
   - `ENABLE_CROSS_SITE_COOKIES`: defina como `true` para permitir que a sessão Flask funcione entre domínios diferentes (Render ↔ Vercel).
   - `SESSION_COOKIE_SECURE`: mantenha `true` em produção (obrigatório quando `ENABLE_CROSS_SITE_COOKIES` estiver ativo).
   > Substitua `https://seu-site.vercel.app` pelo domínio real exibido após o deploy na Vercel. Inclua outras origens (como ambientes de homologação) separadas por vírgula se necessário.
<<<<<<< ours
5. Adicione um **Persistent Disk** com pelo menos 1 GB, montado em `/var/data`, para que o arquivo SQLite não seja perdido a cada deploy. O arquivo `render.yaml` incluso no repositório já descreve essa configuração; basta importá-lo na tela de criação ou mantê-lo no repositório para deploys automatizados.
=======
   > O parâmetro `--root-user-action=ignore` evita o aviso “Running pip as the 'root' user…” que aparece no Render porque o build roda como usuário root.
5. Adicione um **Persistent Disk** (Disco Persistente) com pelo menos 1 GB, montado em `/var/data`, para que o arquivo SQLite não seja perdido a cada deploy. O arquivo `render.yaml` incluso no repositório já descreve essa configuração; basta importá-lo na tela de criação ou mantê-lo no repositório para deploys automatizados.
>>>>>>> theirs
6. Salve e aguarde o Render instalar as dependências, preparar o banco (os dados iniciais são criados automaticamente) e iniciar a API. Ao final, copie a URL pública gerada (por exemplo, `https://biblioteca-backend.onrender.com`).

> Sempre que fizer alterações no backend, um novo deploy será disparado automaticamente. Como o banco está em um disco persistente, os dados inseridos via painel são mantidos entre deploys.

<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
## 5. Abrir no Google Chrome
=======
=======
>>>>>>> theirs
=======
>>>>>>> theirs
## 5. Deploy do frontend na Vercel
1. Acesse o painel da [Vercel](https://vercel.com), clique em **Add New… → Project** e conecte o mesmo repositório.
2. Na etapa **Configure Project**, mantenha o preset **Vite**. **Deixe o campo _Root Directory_ em branco** (ou `.`): como o `package.json` e o código do frontend estão na raiz do repositório, indicar outro caminho — como `render.yaml` ou o próprio nome do repositório — provoca o erro “Root directory must be a subdirectory of the repository”. Caso você já tenha importado o projeto antes com um valor incorreto, abra **Settings → Git** (no painel do projeto) e confirme que o campo **Root Directory** está vazio ou contém apenas `.`; se houver qualquer outro caminho, clique em **Edit** e limpe o valor antes de salvar.
3. Confirme os comandos padrão sugeridos pela Vercel:
   - **Install Command:** `npm install`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
4. Em **Environment Variables**, defina `VITE_API_URL` com a URL pública do backend hospedado no Render (ex.: `https://biblioteca-backend.onrender.com`). O build do frontend usará esse domínio para todas as requisições REST.
5. Salve e aguarde o deploy. Ao final, a Vercel exibirá o domínio `https://…vercel.app`. Teste o site publicado e confirme que as chamadas à API funcionam normalmente.
<<<<<<< ours

## 6. Abrir no Google Chrome
<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
=======
   > Após descobrir o domínio definitivo da Vercel, retorne ao Render, inclua esse endereço na variável `FRONTEND_ORIGIN` (mantendo `http://localhost:5173` para desenvolvimento) e dispare um novo deploy do backend.

## 6. Abrir no Google Chrome
>>>>>>> theirs
=======
## 5. Deploy do frontend na Vercel
1. Acesse o painel da [Vercel](https://vercel.com), clique em **Add New… → Project** (Adicionar novo → Projeto) e conecte o mesmo repositório.
2. Na etapa **Configure Project**, mantenha o preset **Vite**. **Deixe o campo _Root Directory_ em branco** (ou `.`): como o `package.json` e o código do frontend estão na raiz do repositório, indicar outro caminho — como `render.yaml` ou o próprio nome do repositório — provoca o erro “Root directory must be a subdirectory of the repository” ("o diretório raiz precisa ser uma subpasta do repositório"). Caso você já tenha importado o projeto antes com um valor incorreto, abra **Settings → Git** (no painel do projeto) e confirme que o campo **Root Directory** está vazio ou contém apenas `.`; se houver qualquer outro caminho, clique em **Edit** e limpe o valor antes de salvar.
3. Confirme os comandos padrão sugeridos pela Vercel:
   - **Comando de instalação:** `npm install`
   - **Comando de build:** `npm run build`
   - **Diretório de saída:** `dist`
4. Em **Environment Variables** (Variáveis de ambiente), defina `VITE_API_URL` com a URL pública do backend hospedado no Render (ex.: `https://biblioteca-backend.onrender.com`). O build do frontend usará esse domínio para todas as requisições REST.
5. Salve e aguarde o deploy. Ao final, a Vercel exibirá o domínio `https://…vercel.app`. Teste o site publicado e confirme que as chamadas à API funcionam normalmente.
   > Após descobrir o domínio definitivo da Vercel, retorne ao Render, inclua esse endereço na variável `FRONTEND_ORIGIN` (mantendo `http://localhost:5173` para desenvolvimento) e dispare um novo deploy do backend.

## 6. Abrir no Google Chrome
>>>>>>> theirs
- **Modo desenvolvimento:** `http://localhost:5173`
- **Build de produção (preview):** `http://localhost:4173`
- **Servido pelo Flask:** `http://localhost:5000`

Certifique-se de manter o backend rodando em um terminal e o frontend em outro para que todas as rotas funcionem corretamente. Depois de publicar o backend no Render, configure `VITE_API_URL` na Vercel (ou outro host do frontend) usando a URL copiada no passo anterior.
