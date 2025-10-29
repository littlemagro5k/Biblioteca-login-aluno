// Dependências necessárias para montar a tela de boas-vindas.
import React from "react";
import { useNavigate } from "react-router-dom";
import { BookOpen } from "lucide-react";
import "./Welcome.css";

// Tela inicial que incentiva os alunos a explorarem o catálogo.
export default function Welcome() {
  // Hook do React Router responsável por enviar o usuário para a tela de login.
  const navigate = useNavigate();

  return (
    <div className="welcome-page">
      <div className="bg-circle c1"></div>
      <div className="bg-circle c2"></div>

      <div className="welcome-card">
        <div className="icon-wrap">
          {/* Ícone amigável que reforça o tema de leitura */}
          <BookOpen size={64} color="#ffdd55" />
        </div>
        <h1>Bem-vindo ao LeiaSJ!</h1>
        <p>
          Que tal dar uma olhada nos livros que temos disponíveis na biblioteca
          da escola?
        </p>
        {/* Botão que leva o visitante direto ao fluxo de autenticação */}
        <button className="btn-vamos" onClick={() => navigate("/login")}>
          VAMOS LÁ
        </button>
      </div>
    </div>
  );
}
