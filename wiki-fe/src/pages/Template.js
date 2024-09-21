import React from 'react';
import './style/template.css'; 
import logo from './static/logo.png';

function Template({ children }) {
  return (
    <html lang="en">
      <head>
        <title>{/* Replace with your title logic */}</title>
        <link 
          rel="stylesheet" 
          href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" 
          integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" 
          crossOrigin="anonymous" 
        />
        <link rel="icon" href={logo} />
      </head>
      <body>
        <div className="top-bar-container">
          <div className="top-bar">
            <a href="/"> {/* Use anchor tags for navigation */}
              <img src={logo} alt="Wiki Logo" className="wiki-logo" />
            </a>
            <a href="/" className="wiki-title-link">
              <h1 className="wiki-title">WikiDengue</h1>
            </a>
            <form action="/" method="get" className="search-form"> 
              <input className="search" type="text" name="q" placeholder="Pesquisar" />
            </form>

            <div className="top-bar-links">
              <a href="/">Fórum</a>
              <a href="/clima">Clima</a> {/* Adjust href values as needed */}
              <a href="/cadastrar">Cadastrar</a>
              <a href="/entrar">Entrar</a>
            </div>
          </div>
        </div>

        <div className="main-container">
          <div className="row justify-content-center">
            <div className="sidebar-container">
              <div className="sidebar">
                <h2>Navegação</h2>
                <div>
                  <a href="/">Início</a>
                </div>
                <div>
                  <a href="/criar-nova-pagina">Criar nova página</a> 
                </div>
                <div>
                  <a href="/pagina-aleatoria">Random Page</a> 
                </div>
                {/* Add any additional navigation links here */}
              </div>
            </div>

            <div className="main col-lg-10 col-md-9">
              {children} 
            </div>
          </div>
        </div>

        <footer className="footer">
          <div className="footer-content">
            <p>&copy; 2024 WikiDengue. Todos os direitos reservados.</p>
            <p>
              <a href="/contato">Contato</a> | <a href="/sobre">Sobre</a>
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}

export default Template;