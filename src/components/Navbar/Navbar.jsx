// Cabeçalho fixo que exibe a identidade visual do projeto.
// Centralizamos a lógica aqui para facilitar futuras alterações.
import React from "react";
import "./Navbar.css";
import Logo from "../../assets/Logo3.png";

export default function Navbar() {
  return (
    // A tag <header> indica semanticamente que este bloco é um cabeçalho.
    <header className="navbar">
      {/* Logo oficial do projeto, importante para reforçar a marca da escola. */}
      <img src={Logo} alt="Logo LeiaSJ" className="navbar-logo" />
    </header>
  );
}
