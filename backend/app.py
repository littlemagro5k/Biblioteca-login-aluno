import importlib.util
import os
import sqlite3


def _ensure_flask_installed() -> None:
    """Garante que o Flask esteja disponível antes de iniciar a aplicação."""

    if importlib.util.find_spec('flask') is None:
        mensagem = (
            'Flask não está instalado. Execute `pip install -r backend/requeriments.txt` '
            'ou `pip install -r requirements.txt` antes de iniciar o servidor.'
        )
        raise SystemExit(mensagem)


_ensure_flask_installed()

from flask import Flask, jsonify, request, session

try:  # Permite executar como pacote (backend.app) ou script direto.
    from .init_db import criar_banco
except ImportError:  # pragma: no cover - fallback quando executado diretamente
    from init_db import criar_banco

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = 'chave_super_secreta'  # troque por algo seguro

# Caminho do arquivo SQLite que armazena os dados da biblioteca.
DB = 'biblioteca.db'


def _ensure_schema():
    """Garante que o banco exista antes da primeira requisição."""

    try:
        criar_banco()
    except Exception as exc:  # pragma: no cover - log and continue
        raise SystemExit(f'Falha ao preparar o banco de dados: {exc}')


_ensure_schema()


def conectar():
    """Abre uma conexão com o banco SQLite usando dicionários."""

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_livro(row):
    """Transforma um registro de livro em um dicionário pronto para JSON."""

    return {
        'id': row['id'],
        'titulo': row['titulo'],
        'autor': row['autor'] or '',
        'genero': row['genero'] or '',
        'quantidade': row['quantidade'] if row['quantidade'] is not None else 0,
        'capa': row['capa'] or '',
        'ano': row['ano'],
    }


def row_to_aluno(row, include_password=False):
    """Formata os dados de aluno e inclui a senha quando solicitado."""

    return {
        'id': row['id'],
        'nomeCompleto': row['nome_completo'],
        'serie': row['serie'],
        'sala': row['sala'],
        **({'senha': row['senha']} if include_password and 'senha' in row.keys() else {}),
    }


def row_to_bibliotecario(row, include_password=False):
    """Formata os dados do bibliotecário, com senha opcional."""

    payload = {
        'id': row['id'],
        'nomeCompleto': row['nome_completo'],
        'codigo': row['codigo'],
        'turno': (row['turno'] if 'turno' in row.keys() else None) or '',
    }
    if include_password and 'senha' in row.keys():
        payload['senha'] = row['senha']
    return payload


@app.route('/')
def index():
    """Entrega o frontend compilado quando executamos o backend em produção."""

    if app.static_folder:
        index_path = os.path.join(app.static_folder, 'index.html')
        if os.path.exists(index_path):
            return app.send_static_file('index.html')

    mensagem = (
        'Frontend não encontrado. Execute `npm run dev` para desenvolvimento '
        'ou `npm run build` para gerar os arquivos estáticos.'
    )
    return mensagem, 503, {'Content-Type': 'text/plain; charset=utf-8'}


@app.route('/api/bibliotecario/login', methods=['POST'])
def login_bibliotecario():
    """Realiza o login de bibliotecários e cria uma sessão baseada em cookies."""

    data = request.get_json() or {}
    nome = (data.get('nomeCompleto') or '').strip()
    codigo = (data.get('codigo') or '').strip()
    senha = data.get('senha') or ''

    if not nome or not codigo or not senha:
        return jsonify({'erro': 'Nome completo, código e senha são obrigatórios.'}), 400

    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        '''
        SELECT id, nome_completo, codigo
        FROM bibliotecarios
        WHERE lower(nome_completo) = lower(?)
          AND codigo = ?
          AND senha = ?
        ''',
        (nome, codigo, senha),
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify({'erro': 'Bibliotecário não encontrado ou dados inválidos.'}), 401

    session['bibliotecario_id'] = row['id']
    session['bibliotecario_nome'] = row['nome_completo']

    return jsonify(
        {
            'mensagem': 'Login realizado com sucesso!',
            'bibliotecario': {
                'id': row['id'],
                'nomeCompleto': row['nome_completo'],
                'codigo': row['codigo'],
            },
        }
    )


def _listar_alunos():
    """Retorna alunos cadastrados filtrando por nome quando necessário."""

    if 'bibliotecario_id' not in session:
        return jsonify({'erro': 'Não autorizado'}), 403

    busca = (request.args.get('busca') or '').strip().lower()

    conn = conectar()
    cur = conn.cursor()

    if busca:
        like_term = f'%{busca}%'
        cur.execute(
            '''
            SELECT id, nome_completo, serie, sala, senha
            FROM alunos
            WHERE lower(nome_completo) LIKE ?
            ORDER BY nome_completo COLLATE NOCASE
            ''',
            (like_term,),
        )
    else:
        cur.execute(
            '''
            SELECT id, nome_completo, serie, sala, senha
            FROM alunos
            ORDER BY nome_completo COLLATE NOCASE
            '''
        )

    alunos = [row_to_aluno(row, include_password=True) for row in cur.fetchall()]
    conn.close()
    return jsonify(alunos)


def _cadastrar_aluno():
    """Insere um novo aluno garantindo integridade das informações."""

    data = request.get_json() or {}
    nome = (data.get('nomeCompleto') or '').strip()
    serie = (data.get('serie') or '').strip()
    sala = (data.get('sala') or '').strip()
    senha = data.get('senha') or ''

    if not nome or not serie or not sala or not senha:
        return jsonify({'erro': 'Nome, série, sala e senha são obrigatórios.'}), 400
    if len(senha) < 4:
        return jsonify({'erro': 'A senha deve ter pelo menos 4 caracteres.'}), 400

    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        '''
        SELECT id
        FROM alunos
        WHERE lower(nome_completo) = lower(?)
          AND serie = ?
          AND sala = ?
        ''',
        (nome, serie, sala),
    )
    if cur.fetchone():
        conn.close()
        return jsonify({'erro': 'Aluno já cadastrado para esta turma.'}), 409

    cur.execute(
        '''
        INSERT INTO alunos (nome_completo, serie, sala, senha)
        VALUES (?, ?, ?, ?)
        ''',
        (nome, serie, sala, senha),
    )
    aluno_id = cur.lastrowid
    conn.commit()

    cur.execute(
        'SELECT id, nome_completo, serie, sala FROM alunos WHERE id = ?',
        (aluno_id,),
    )
    aluno = cur.fetchone()
    conn.close()

    return (
        jsonify(
            {
                'mensagem': 'Aluno cadastrado com sucesso!',
                'aluno': row_to_aluno(aluno),
            }
        ),
        201,
    )


@app.route('/api/alunos', methods=['GET', 'POST'])
def gerenciar_alunos():
    """Agrupa listagem e criação de alunos no mesmo endpoint."""

    if request.method == 'POST':
        return _cadastrar_aluno()
    return _listar_alunos()


@app.route('/api/alunos/<int:aluno_id>', methods=['PUT'])
def atualizar_aluno(aluno_id):
    """Atualiza campos enviados pelo painel do bibliotecário."""

    if 'bibliotecario_id' not in session:
        return jsonify({'erro': 'Não autorizado'}), 403

    data = request.get_json() or {}
    campos = {}

    if 'nomeCompleto' in data:
        nome = (data.get('nomeCompleto') or '').strip()
        if not nome:
            return jsonify({'erro': 'Nome completo é obrigatório.'}), 400
        campos['nome_completo'] = nome

    if 'serie' in data:
        serie = (data.get('serie') or '').strip()
        if not serie:
            return jsonify({'erro': 'Série é obrigatória.'}), 400
        campos['serie'] = serie

    if 'sala' in data:
        sala = (data.get('sala') or '').strip()
        if not sala:
            return jsonify({'erro': 'Sala é obrigatória.'}), 400
        campos['sala'] = sala

    if 'senha' in data:
        senha = data.get('senha') or ''
        if len(senha) < 4:
            return jsonify({'erro': 'A senha deve ter pelo menos 4 caracteres.'}), 400
        campos['senha'] = senha

    if not campos:
        return jsonify({'erro': 'Nenhum dado para atualizar.'}), 400

    conn = conectar()
    cur = conn.cursor()

    cur.execute('SELECT id FROM alunos WHERE id = ?', (aluno_id,))
    if cur.fetchone() is None:
        conn.close()
        return jsonify({'erro': 'Aluno não encontrado.'}), 404

    updates = ', '.join(f"{col} = ?" for col in campos)
    cur.execute(
        f'UPDATE alunos SET {updates} WHERE id = ?',
        (*campos.values(), aluno_id),
    )
    conn.commit()

    cur.execute(
        'SELECT id, nome_completo, serie, sala, senha FROM alunos WHERE id = ?',
        (aluno_id,),
    )
    aluno = cur.fetchone()
    conn.close()

    if aluno is None:
        return jsonify({'erro': 'Aluno não encontrado.'}), 404

    return jsonify({'mensagem': 'Aluno atualizado com sucesso!', 'aluno': row_to_aluno(aluno, include_password=True)})


@app.route('/api/alunos/<int:aluno_id>', methods=['DELETE'])
def excluir_aluno(aluno_id):
    """Remove definitivamente um aluno da base de dados."""

    if 'bibliotecario_id' not in session:
        return jsonify({'erro': 'Não autorizado'}), 403

    conn = conectar()
    cur = conn.cursor()
    cur.execute('DELETE FROM alunos WHERE id = ?', (aluno_id,))

    if cur.rowcount == 0:
        conn.close()
        return jsonify({'erro': 'Aluno não encontrado.'}), 404

    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Aluno removido com sucesso!'})


@app.route('/api/alunos/login', methods=['POST'])
def login_aluno():
    """Autentica estudantes para acesso ao catálogo de livros."""

    data = request.get_json() or {}
    nome = (data.get('nomeCompleto') or '').strip()
    senha = data.get('senha') or ''

    if not nome or not senha:
        return jsonify({'erro': 'Nome completo e senha são obrigatórios.'}), 400

    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        '''
        SELECT id, nome_completo, serie, sala
        FROM alunos
        WHERE lower(nome_completo) = lower(?)
          AND senha = ?
        ''',
        (nome, senha),
    )
    aluno = cur.fetchone()
    conn.close()

    if not aluno:
        return jsonify({'erro': 'Aluno não encontrado ou senha incorreta.'}), 401

    return jsonify(row_to_aluno(aluno))


def _listar_bibliotecarios():
    """Lista bibliotecários filtrando por nome ou código quando informado."""

    if 'bibliotecario_id' not in session:
        return jsonify({'erro': 'Não autorizado'}), 403

    busca = (request.args.get('busca') or '').strip().lower()

    conn = conectar()
    cur = conn.cursor()

    if busca:
        like_term = f'%{busca}%'
        cur.execute(
            '''
            SELECT id, nome_completo, codigo, turno, senha
            FROM bibliotecarios
            WHERE lower(nome_completo) LIKE ? OR lower(codigo) LIKE ?
            ORDER BY nome_completo COLLATE NOCASE
            ''',
            (like_term, like_term),
        )
    else:
        cur.execute(
            '''
            SELECT id, nome_completo, codigo, turno, senha
            FROM bibliotecarios
            ORDER BY nome_completo COLLATE NOCASE
            '''
        )

    bibliotecarios = [
        row_to_bibliotecario(row, include_password=True) for row in cur.fetchall()
    ]
    conn.close()
    return jsonify(bibliotecarios)


def _cadastrar_bibliotecario():
    """Adiciona um bibliotecário novo garantindo código exclusivo."""

    if 'bibliotecario_id' not in session:
        return jsonify({'erro': 'Não autorizado'}), 403

    data = request.get_json() or {}
    nome = (data.get('nomeCompleto') or '').strip()
    codigo = (data.get('codigo') or '').strip()
    senha = (data.get('senha') or '').strip()
    turno = (data.get('turno') or '').strip() or None

    if not nome or not codigo or not senha:
        return jsonify({'erro': 'Nome completo, código e senha são obrigatórios.'}), 400
    if len(senha) < 4:
        return jsonify({'erro': 'A senha deve ter pelo menos 4 caracteres.'}), 400

    conn = conectar()
    cur = conn.cursor()

    cur.execute(
        'SELECT id FROM bibliotecarios WHERE codigo = ?',
        (codigo,),
    )
    if cur.fetchone():
        conn.close()
        return jsonify({'erro': 'Já existe um bibliotecário cadastrado com esse código.'}), 409

    cur.execute(
        '''
        INSERT INTO bibliotecarios (nome_completo, codigo, senha, turno)
        VALUES (?, ?, ?, ?)
        ''',
        (nome, codigo, senha, turno),
    )
    bibliotecario_id = cur.lastrowid
    conn.commit()

    cur.execute(
        'SELECT id, nome_completo, codigo, turno, senha FROM bibliotecarios WHERE id = ?',
        (bibliotecario_id,),
    )
    row = cur.fetchone()
    conn.close()

    return (
        jsonify(
            {
                'mensagem': 'Bibliotecário cadastrado com sucesso!',
                'bibliotecario': row_to_bibliotecario(row, include_password=True),
            }
        ),
        201,
    )


def _atualizar_bibliotecario(bibliotecario_id):
    """Atualiza os dados de um bibliotecário existente."""

    if 'bibliotecario_id' not in session:
        return jsonify({'erro': 'Não autorizado'}), 403

    data = request.get_json() or {}
    campos = {}

    if 'nomeCompleto' in data:
        nome = (data.get('nomeCompleto') or '').strip()
        if not nome:
            return jsonify({'erro': 'Nome completo é obrigatório.'}), 400
        campos['nome_completo'] = nome

    if 'codigo' in data:
        codigo = (data.get('codigo') or '').strip()
        if not codigo:
            return jsonify({'erro': 'Código é obrigatório.'}), 400
        campos['codigo'] = codigo

    if 'senha' in data:
        senha = (data.get('senha') or '').strip()
        if len(senha) < 4:
            return jsonify({'erro': 'A senha deve ter pelo menos 4 caracteres.'}), 400
        campos['senha'] = senha

    if 'turno' in data:
        turno = (data.get('turno') or '').strip()
        campos['turno'] = turno or None

    if not campos:
        return jsonify({'erro': 'Nenhum dado para atualizar.'}), 400

    conn = conectar()
    cur = conn.cursor()

    cur.execute('SELECT id FROM bibliotecarios WHERE id = ?', (bibliotecario_id,))
    if cur.fetchone() is None:
        conn.close()
        return jsonify({'erro': 'Bibliotecário não encontrado.'}), 404

    if 'codigo' in campos:
        cur.execute(
            'SELECT id FROM bibliotecarios WHERE codigo = ? AND id != ?',
            (campos['codigo'], bibliotecario_id),
        )
        if cur.fetchone() is not None:
            conn.close()
            return jsonify({'erro': 'Já existe um bibliotecário cadastrado com esse código.'}), 409

    updates = ', '.join(f"{col} = ?" for col in campos)
    cur.execute(
        f'UPDATE bibliotecarios SET {updates} WHERE id = ?',
        (*campos.values(), bibliotecario_id),
    )
    conn.commit()

    cur.execute(
        'SELECT id, nome_completo, codigo, turno, senha FROM bibliotecarios WHERE id = ?',
        (bibliotecario_id,),
    )
    row = cur.fetchone()
    conn.close()

    if row is None:
        return jsonify({'erro': 'Bibliotecário não encontrado.'}), 404

    return jsonify(
        {
            'mensagem': 'Bibliotecário atualizado com sucesso!',
            'bibliotecario': row_to_bibliotecario(row, include_password=True),
        }
    )


def _excluir_bibliotecario(bibliotecario_id):
    """Remove um bibliotecário do sistema."""

    if 'bibliotecario_id' not in session:
        return jsonify({'erro': 'Não autorizado'}), 403

    conn = conectar()
    cur = conn.cursor()
    cur.execute('DELETE FROM bibliotecarios WHERE id = ?', (bibliotecario_id,))

    if cur.rowcount == 0:
        conn.close()
        return jsonify({'erro': 'Bibliotecário não encontrado.'}), 404

    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Bibliotecário removido com sucesso!'})


@app.route('/api/bibliotecarios', methods=['GET', 'POST'])
def gerenciar_bibliotecarios():
    """Endpoint responsável por listar ou criar bibliotecários."""

    if request.method == 'POST':
        return _cadastrar_bibliotecario()
    return _listar_bibliotecarios()


@app.route('/api/bibliotecarios/<int:bibliotecario_id>', methods=['PUT', 'DELETE'])
def modificar_bibliotecario(bibliotecario_id):
    """Escolhe entre atualizar ou excluir de acordo com o método HTTP."""

    if request.method == 'PUT':
        return _atualizar_bibliotecario(bibliotecario_id)
    return _excluir_bibliotecario(bibliotecario_id)


@app.route('/logout', methods=['POST'])
def logout():
    """Encerra a sessão do bibliotecário removendo dados da Flask session."""

    session.pop('bibliotecario_id', None)
    session.pop('bibliotecario_nome', None)
    return jsonify({'mensagem': 'Logout realizado'})


@app.route('/api/livros', methods=['GET'])
def listar_livros():
    """Retorna livros cadastrados permitindo busca por título ou autor."""

    busca = request.args.get('busca', '').strip()
    conn = conectar()
    cur = conn.cursor()

    if busca:
        like_term = f'%{busca}%'
        cur.execute(
            """
            SELECT id, titulo, autor, genero, quantidade, capa, ano
            FROM livros
            WHERE titulo LIKE ? OR autor LIKE ?
            ORDER BY titulo COLLATE NOCASE
            """,
            (like_term, like_term),
        )
    else:
        cur.execute(
            """
            SELECT id, titulo, autor, genero, quantidade, capa, ano
            FROM livros
            ORDER BY titulo COLLATE NOCASE
            """
        )

    livros = [row_to_livro(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(livros)


@app.route('/api/livros', methods=['POST'])
def adicionar_livro():
    """Cadastra um novo livro validando quantidade e ano."""

    if 'bibliotecario_id' not in session:
        return jsonify({'erro': 'Não autorizado'}), 403

    data = request.get_json() or {}
    titulo = (data.get('titulo') or '').strip()
    if not titulo:
        return jsonify({'erro': 'Título é obrigatório'}), 400

    autor = (data.get('autor') or '').strip()
    genero = (data.get('genero') or '').strip()
    capa = (data.get('capa') or '').strip()
    ano = data.get('ano')
    ano_int = None
    if ano not in (None, ''):
        try:
            ano_int = int(ano)
        except (TypeError, ValueError):
            return jsonify({'erro': 'Ano inválido'}), 400

    quantidade = data.get('quantidade', 0)
    try:
        quantidade_int = int(quantidade)
    except (TypeError, ValueError):
        return jsonify({'erro': 'Quantidade inválida'}), 400

    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO livros (titulo, autor, genero, quantidade, capa, ano)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (titulo, autor, genero, quantidade_int, capa, ano_int),
    )
    novo_id = cur.lastrowid
    conn.commit()

    cur.execute(
        "SELECT id, titulo, autor, genero, quantidade, capa, ano FROM livros WHERE id = ?",
        (novo_id,),
    )
    livro = cur.fetchone()
    conn.close()

    return (
        jsonify({'mensagem': 'Livro adicionado com sucesso!', 'livro': row_to_livro(livro)}),
        201,
    )


@app.route('/api/livros/<int:livro_id>', methods=['PUT'])
def atualizar_livro(livro_id):
    """Atualiza campos do livro escolhendo apenas o que foi enviado."""

    if 'bibliotecario_id' not in session:
        return jsonify({'erro': 'Não autorizado'}), 403

    data = request.get_json() or {}
    campos_validos = {
        'titulo': lambda v: (v or '').strip(),
        'autor': lambda v: (v or '').strip(),
        'genero': lambda v: (v or '').strip(),
        'capa': lambda v: (v or '').strip(),
        'ano': lambda v: v,
        'quantidade': lambda v: v,
    }

    updates = []
    valores = []

    for campo, normalizer in campos_validos.items():
        if campo not in data:
            continue
        valor = normalizer(data.get(campo))
        if campo == 'ano':
            if valor in (None, ''):
                valor = None
            else:
                try:
                    valor = int(valor)
                except (TypeError, ValueError):
                    return jsonify({'erro': 'Ano inválido'}), 400
        if campo == 'quantidade':
            try:
                valor = int(valor)
            except (TypeError, ValueError):
                return jsonify({'erro': 'Quantidade inválida'}), 400
        updates.append(f"{campo} = ?")
        valores.append(valor)

    if not updates:
        return jsonify({'erro': 'Nenhum dado para atualizar'}), 400

    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE livros SET {', '.join(updates)} WHERE id = ?",
        (*valores, livro_id),
    )

    if cur.rowcount == 0:
        conn.close()
        return jsonify({'erro': 'Livro não encontrado'}), 404

    conn.commit()
    cur.execute(
        "SELECT id, titulo, autor, genero, quantidade, capa, ano FROM livros WHERE id = ?",
        (livro_id,),
    )
    livro = cur.fetchone()
    conn.close()

    return jsonify({'mensagem': 'Livro atualizado com sucesso!', 'livro': row_to_livro(livro)})


@app.route('/api/livros/<int:livro_id>', methods=['DELETE'])
def excluir_livro(livro_id):
    """Exclui um livro e retorna erro apropriado quando não encontrado."""

    if 'bibliotecario_id' not in session:
        return jsonify({'erro': 'Não autorizado'}), 403

    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
    if cur.rowcount == 0:
        conn.close()
        return jsonify({'erro': 'Livro não encontrado'}), 404

    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Livro removido com sucesso!'})


if __name__ == '__main__':
    if not os.path.exists(DB):
        print('Banco não encontrado. Criando automaticamente...')
        from init_db import criar_banco

        criar_banco()
    app.run(debug=True)
