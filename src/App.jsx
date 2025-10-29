// Componente raiz que organiza a navegação entre todas as páginas do site.
// Aqui ficam centralizadas as rotas e o cabeçalho fixo (Navbar).
import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar/Navbar";

// Importamos as páginas principais disponíveis para alunos e bibliotecários.
import Welcome from "./pages/Welcome/Welcome";
import Login from "./pages/Login/Login";
import Usuario from "./pages/Usuario/Usuario";
import Bibliotecario from "./pages/Bibliotecario/Bibliotecario";

export default function App() {
  return (
    <>
      {/* Barra superior exibida em todas as telas do aplicativo. */}
      <Navbar />

      {/* Container central onde as páginas são renderizadas conforme a rota. */}
      <div className="container py-3">
        <Routes>
          {/* Rota da página de boas-vindas apresentada na entrada do site. */}
          <Route path="/" element={<Welcome />} />

          {/* Demais páginas acessíveis via menu ou redirecionamentos. */}
          <Route path="/login" element={<Login />} />
          <Route path="/usuario" element={<Usuario />} />
          <Route path="/bibliotecario" element={<Bibliotecario />} />

          {/* Fallback: qualquer URL desconhecida leva o usuário de volta ao início. */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </>
  );
}
