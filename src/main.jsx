// Arquivo responsável por inicializar todo o front-end da aplicação.
// Aqui importamos as dependências essenciais do React e definimos o ponto
// exato onde o aplicativo será renderizado dentro da página HTML.
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App.jsx";
import "./index.css";

// O ReactDOM.createRoot cria o vínculo entre o React e a div "root" do
// arquivo index.html. A partir desse ponto, todo o conteúdo do App.jsx será
// exibido na tela.
ReactDOM.createRoot(document.getElementById("root")).render(
  // StrictMode habilita verificações extras em modo desenvolvimento, ajudando
  // a detectar problemas comuns como efeitos colaterais não tratados.
  <React.StrictMode>
    {/* BrowserRouter habilita a navegação por rotas (URLs) dentro do app. */}
    <BrowserRouter>
      {/* App é o componente principal que contém todas as rotas e páginas. */}
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
