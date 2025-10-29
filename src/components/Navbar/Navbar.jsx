// Importa o React para declarar o componente funcional.
import React from "react";
// Estilos específicos da barra de navegação.
import "./Navbar.css";
// Logotipo exibido no cabeçalho.
import Logo from "../../assets/Logo3.png";

// Cabeçalho minimalista exibido em todas as telas do sistema.
export default function Navbar() {
  return (
    <header className="navbar">
      {/* A imagem da marca ajuda na identificação do projeto pelos estudantes */}
      <img src={Logo} alt="Logo LeiaSJ" className="navbar-logo" />
    </header>
  );
}
