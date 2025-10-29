// Hooks e ícones utilizados na área do aluno/funcionário.
import React, { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { Bell, User, AlertTriangle } from "lucide-react";
import "./Usuario.css";
import { fetchBooks } from "../../services/api";

// Painel voltado ao estudante/funcionário que consulta o catálogo de livros.
export default function Usuario() {
  // Catálogo carregado da API ou do cache.
  const [livros, setLivros] = useState([]);
  // Dados do usuário atualmente logado.
  const [usuario, setUsuario] = useState(null);
  // Lista de notificações relacionadas a prazos de empréstimo.
  const [notificacoes, setNotificacoes] = useState([]);
  // Estado que controla a abertura do painel de notificações.
  const [mostrarNotificacoes, setMostrarNotificacoes] = useState(false);
  const navigate = useNavigate();

  // === Carrega usuário e livros ===
  useEffect(() => {
    const userData = JSON.parse(localStorage.getItem("leiasj_logged_user"));
    if (!userData) {
      navigate("/login");
      return;
    }
    setUsuario(userData);
    const livrosSalvos =
      JSON.parse(localStorage.getItem("leiasj_books_v1")) || [];
    if (livrosSalvos.length) {
      setLivros(livrosSalvos);
    }

    fetchBooks()
      .then((dados) => {
        setLivros(dados);
        localStorage.setItem("leiasj_books_v1", JSON.stringify(dados));
      })
      .catch((error) => {
        console.error("Erro ao sincronizar catálogo", error);
      });
  }, [navigate]);

  // === Solicitação de empréstimo ===
  // Salva um pedido de empréstimo no localStorage para o bibliotecário analisar.
  const solicitarEmprestimo = (livro) => {
    if (!usuario) return alert("Você precisa estar logado para solicitar.");
    if (Number(livro.quantidade) <= 0) {
      alert(`O livro "${livro.titulo}" não está disponível no momento.`);
      return;
    }

    const emprestimos =
      JSON.parse(localStorage.getItem("leiasj_loans_v1")) || [];
    const novoEmprestimo = {
      id: Date.now(),
      usuario: { nome: usuario.nome, tipo: usuario.tipo },
      livro: { titulo: livro.titulo, id: livro.id },
      dataEmprestimo: new Date().toLocaleDateString("pt-BR"),
      prazo: "A definir",
      status: "Pendente",
    };
    emprestimos.push(novoEmprestimo);
    localStorage.setItem("leiasj_loans_v1", JSON.stringify(emprestimos));
    alert("Solicitação enviada para o bibliotecário!");
  };

  // === Verificação de prazos ===
  // Analisa periodicamente os empréstimos do usuário para avisar sobre prazos.
  const verificarPrazos = useCallback(() => {
    const emprestimos =
      JSON.parse(localStorage.getItem("leiasj_loans_v1")) || [];
    const meus = emprestimos.filter(
      (e) => e.usuario?.nome === usuario?.nome && e.status === "Emprestado"
    );

    const hoje = new Date();
    const novas = [];

    meus.forEach((e) => {
      if (!e.prazo || e.prazo === "A definir") return;
      const prazo = new Date(e.prazo);
      const diff = Math.ceil((prazo - hoje) / (1000 * 60 * 60 * 24));
      if (diff <= 3 && diff >= 0) {
        novas.push({
          id: e.id,
          livro: e.livro?.titulo,
          dias: diff,
        });
      }
    });

    setNotificacoes(novas);
  }, [usuario]);

  useEffect(() => {
    if (!usuario) return;
    verificarPrazos();
    const interval = setInterval(verificarPrazos, 15000);
    return () => clearInterval(interval);
  }, [usuario, verificarPrazos]);

  // === Logout ===
  // Remove o registro local da sessão e retorna para a tela de login.
  const handleLogout = () => {
    if (window.confirm("Tem certeza que deseja sair?")) {
      localStorage.removeItem("leiasj_logged_user");
      navigate("/login");
    }
  };

  return (
    <div className="usuario-page">
      {/* Cabeçalho com identificação do usuário e ícones de alerta */}
      <header className="usuario-header">
        <h2>Catálogo de Livros</h2>
        {usuario && (
          <div className="usuario-info">
            <div className="user-icon">
              <User size={18} />
              <span>{usuario.nome}</span>
            </div>

            {/* 🔔 Sino de notificação */}
            <div className="notif-wrapper">
              <button
                className={`btn-bell ${notificacoes.length > 0 ? "ativo" : ""}`}
                onClick={() => setMostrarNotificacoes((v) => !v)}
                aria-label="Notificações"
              >
                <Bell size={22} />
                {notificacoes.length > 0 && (
                  <span className="badge-dot">{notificacoes.length}</span>
                )}
              </button>

              {mostrarNotificacoes && (
                <div className="notif-panel">
                  <div className="notif-head">
                    <strong>Notificações</strong>
                    <button
                      className="btn-mini"
                      onClick={() => setNotificacoes([])}
                    >
                      Limpar
                    </button>
                  </div>
                  <ul>
                    {notificacoes.length === 0 ? (
                      <li className="n-info">Nenhum alerta no momento.</li>
                    ) : (
                      notificacoes.map((n) => (
                        <li key={n.id} className="n-warning">
                          <AlertTriangle
                            size={16}
                            color="#ffdd55"
                            style={{ marginRight: "6px" }}
                          />
                          <span className="n-text">
                            O prazo de <b>{n.livro}</b> termina em{" "}
                            <b>{n.dias}</b> dia{n.dias > 1 ? "s" : ""}.
                          </span>
                        </li>
                      ))
                    )}
                  </ul>
                </div>
              )}
            </div>

            <button className="btn-sair" onClick={handleLogout}>
              Sair
            </button>
          </div>
        )}
      </header>

      {livros.length === 0 ? (
        <p className="texto-vazio">Nenhum livro disponível no momento.</p>
      ) : (
        <div className="livros-grid">
          {livros.map((livro) => {
            const indisponivel = Number(livro.quantidade) <= 0;
            return (
              <div key={livro.id} className="livro-card">
                {/* Exibe a capa cadastrada ou uma imagem genérica caso não exista */}
                <img
                  src={
                    livro.capa ||
                    "https://via.placeholder.com/120x160?text=Sem+Capa"
                  }
                  alt={livro.titulo}
                />
                <h4 title={livro.titulo}>{livro.titulo}</h4>
                <p className="autor">{livro.autor}</p>
                <p>
                  <strong>Gênero:</strong> {livro.genero}
                </p>
                <p>
                  <strong>Ano:</strong> {livro.ano ?? "Não informado"}
                </p>
                <p className="qtd">
                  <strong>Disponíveis:</strong> {livro.quantidade}
                </p>

                {indisponivel && (
                  <div className="badge-indisponivel">
                    Não disponível no momento
                  </div>
                )}

                <button
                  className="btn btn-warning btn-sm mt-2"
                  onClick={() => solicitarEmprestimo(livro)}
                  disabled={indisponivel}
                >
                  {indisponivel ? "Indisponível" : "Solicitar Empréstimo"}
                </button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
