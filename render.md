# Guia de Deploy no Render

Este guia detalha como publicar o backend Flask deste projeto no Render utilizando o arquivo `render.yaml` incluído no repositório.

## 1. Preparar o repositório
- Garanta que todo o código esteja versionado e disponível em um repositório Git (GitHub, GitLab ou Bitbucket).
- Confirme que o arquivo `render.yaml` esteja na raiz do projeto para facilitar a importação das configurações.

## 2. Criar um serviço Web no Render
1. Acesse o painel do [Render](https://render.com) com a sua conta.
2. Clique em **New + → Web Service** e conecte o repositório que contém o projeto.
3. Quando o Render detectar o projeto, ele sugerirá automaticamente o runtime **Python** por conta do `requirements.txt`.

## 3. Comandos de build e execução
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn backend.app:app`

Esses comandos já estão descritos no `render.yaml` e são suficientes para instalar as dependências e iniciar o servidor WSGI.

## 4. Deploy do backend no Render
1. Faça o push do repositório para o GitHub (ou outro provedor) contendo este projeto.
2. Com a conta criada no Render, clique em **New + → Web Service** e conecte o repositório.
3. Quando o Render detectar o projeto, confirme as opções:
   - **Runtime**: Python (detectado automaticamente por causa do `requirements.txt`).
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn backend.app:app`
<<<<<<< ours
4. Em **Environment Variables**, garanta que exista uma variável `FLASK_SECRET_KEY`. Você pode usar o botão *Generate* ou definir um valor próprio. Caso deseje armazenar o banco em um volume persistente, crie também a variável `DATABASE_PATH` apontando para `/var/data/biblioteca.db`.
5. Adicione um **Persistent Disk** com pelo menos 1 GB, montado em `/var/data`, para que o arquivo SQLite não seja perdido a cada deploy. O arquivo `render.yaml` incluso no repositório já descreve essa configuração; basta importá-lo na tela de criação ou mantê-lo no repositório para deploys automatizados.
6. Salve e aguarde o Render instalar as dependências, preparar o banco (os dados iniciais são criados automaticamente) e iniciar a API. Ao final, copie a URL pública gerada (por exemplo, `https://biblioteca-backend.onrender.com`).
=======
4. Em **Environment Variables**, configure:
   - `FLASK_SECRET_KEY`: gere pelo botão *Generate* ou informe um valor forte.
   - `DATABASE_PATH`: defina como `/var/data/biblioteca.db` para usar o disco persistente.
   - `FRONTEND_ORIGIN`: liste os domínios que podem chamar a API (ex.: `https://seu-site.vercel.app,http://localhost:5173`).
   - `ENABLE_CROSS_SITE_COOKIES`: coloque `true` para liberar a sessão entre Render e Vercel.
   - `SESSION_COOKIE_SECURE`: mantenha `true` em produção (obrigatório quando o item anterior está ativo).
   > Ajuste `https://seu-site.vercel.app` para o domínio real fornecido pela Vercel e adicione outras origens necessárias separadas por vírgula.
5. Adicione um **Persistent Disk** com pelo menos 1 GB, montado em `/var/data`, para que o arquivo SQLite não seja perdido a cada deploy. O arquivo `render.yaml` incluso no repositório já descreve essa configuração; basta importá-lo na tela de criação ou mantê-lo no repositório para deploys automatizados.
6. Salve e aguarde o Render instalar as dependências, preparar o banco (os dados iniciais são criados automaticamente) e iniciar a API. Ao final, copie a URL pública gerada (por exemplo, `https://biblioteca-backend.onrender.com`).
   > Assim que o domínio da Vercel estiver disponível, acrescente-o na variável `FRONTEND_ORIGIN` e faça o redeploy do backend para liberar as chamadas do frontend hospedado.
>>>>>>> theirs

> Sempre que fizer alterações no backend, um novo deploy será disparado automaticamente. Como o banco está em um disco persistente, os dados inseridos via painel são mantidos entre deploys.

## 5. Atualizar o frontend
- Configure a variável de ambiente `VITE_API_URL` na Vercel (ou em outro host do frontend) apontando para a URL pública gerada pelo Render.
- Refaça o deploy do frontend para que as chamadas REST sejam direcionadas ao backend recém-publicado.

## 6. Manutenção
- O Render manterá os dados do SQLite no disco persistente enquanto o serviço estiver ativo.
- Revise periodicamente as variáveis de ambiente e tokens armazenados.
- Para atualizar o backend, basta enviar novas alterações ao repositório; o Render recriará o container e aplicará a nova versão automaticamente.
