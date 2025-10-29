// Importa o núcleo do React utilizado pelo modo estrito.
import React from "react";
// Cliente responsável por "montar" o React dentro do DOM.
import ReactDOM from "react-dom/client";
// Fornece o contexto de rotas para toda a aplicação.
import { BrowserRouter } from "react-router-dom";
// Componente principal da aplicação.
import App from "./App.jsx";
// Estilos globais compartilhados por todas as telas.
import "./index.css";

// Localizamos o elemento <div id="root"> gerado pelo Vite no index.html.
const rootElement = document.getElementById("root");

// Criamos a "raiz" React e renderizamos a aplicação dentro do modo estrito,
// que ajuda a identificar comportamentos inesperados durante o desenvolvimento.
ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    {/* O BrowserRouter injeta a capacidade de navegar entre as rotas definidas */}
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
