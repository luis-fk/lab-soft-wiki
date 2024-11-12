"use client"

import { createContext, useState } from "react";

// Define o contexto a ser utilizado para pegar os parametros article e handleArticle e exporta
export const ArticleContext = createContext();

function ArticleProvider({ children }){
    const [article, setArticle] = useState({});

    // Função que seta o artigo a ser editado
    function handleArticle(title, text, articleId){
        if(articleId >= 0){
            //cria o artigo e salva em article
            setArticle({
                title: title, 
                text: text, 
                articleId: articleId
            });
        }
    }

    // Recebe o children e só renderiza ele
    return(
            <ArticleContext.Provider value={{handleArticle, article}}>
                { children }
            </ArticleContext.Provider>
    );
}

export default ArticleProvider;