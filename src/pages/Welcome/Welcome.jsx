// Página inicial com a mensagem de boas-vindas para os usuários do sistema.
// O objetivo principal é apresentar o projeto e conduzir o visitante ao login.
import React from "react";
import { useNavigate } from "react-router-dom";
import { BookOpen } from "lucide-react";
import "./Welcome.css";

export default function Welcome() {
  const navigate = useNavigate();

  return (
    <div className="welcome-page">
      {/* Elementos de fundo responsáveis pelos círculos decorativos. */}
      <div className="bg-circle c1"></div>
      <div className="bg-circle c2"></div>

      <div className="welcome-card">
        {/* Ícone ilustrativo que reforça o tema da leitura. */}
        <div className="icon-wrap">
          <BookOpen size={64} color="#ffdd55" />
        </div>
        <h1>Bem-vindo ao LeiaSJ!</h1>
        <p>
          Que tal dar uma olhada nos livros que temos disponíveis na biblioteca
          da escola?
        </p>
        {/* Botão que leva o usuário para a tela de login/cadastro. */}
        <button className="btn-vamos" onClick={() => navigate("/login")}>
          VAMOS LÁ
        </button>
      </div>
    </div>
  );
}
