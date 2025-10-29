// Importamos o núcleo do React para poder declarar componentes funcionais.
import React from "react";
// A partir do React Router, trazemos os componentes responsáveis por montar a
// navegação declarativa da aplicação.
import { Routes, Route, Navigate } from "react-router-dom";
// Barra fixa exibida em todas as telas.
import Navbar from "./components/Navbar/Navbar";

// 🌟 Páginas principais da aplicação. Cada import corresponde a uma rota.
import Welcome from "./pages/Welcome/Welcome";
import Login from "./pages/Login/Login";
import Usuario from "./pages/Usuario/Usuario";
import Bibliotecario from "./pages/Bibliotecario/Bibliotecario";

// Componente raiz responsável por renderizar a estrutura base e mapear as rotas.
export default function App() {
  return (
    <>
      {/* A navbar fica fora das rotas para permanecer fixa em todas as páginas */}
      <Navbar />
      <div className="container py-3">
        <Routes>
          {/* Página inicial: apresenta o projeto e um botão para ir ao login */}
          <Route path="/" element={<Welcome />} />

          {/* Fluxos de autenticação dos três perfis do sistema */}
          <Route path="/login" element={<Login />} />
          <Route path="/usuario" element={<Usuario />} />
          <Route path="/bibliotecario" element={<Bibliotecario />} />

          {/* Qualquer rota inválida redireciona gentilmente para a página inicial */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </>
  );
}
