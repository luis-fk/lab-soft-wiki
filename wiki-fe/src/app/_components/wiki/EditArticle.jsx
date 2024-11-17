"use client"
import React, { useState, useEffect } from 'react';
import { getSession } from '@/lib/session';
import { useRouter } from 'next/navigation';
import "@/styles/wiki/new-article.css";
import ErrorMessage from "@/app/_components/auth/ErrorMessage";

// Importes do Context 
import { ArticleContext } from '@/app/contexts/articleProvider';
import { useContext } from 'react';

import useMarkdownToHtml from '@/hooks/markdownToHtml';


export default function EditArticle() {
    const router = useRouter();
    const [text, setText] = useState('');
    const [title, setTitle] = useState('');
    const [articleId, setArticleId] = useState('');
    const [errorMessage, setErrorMessage] = useState(null);

    // utilizo { article } pra pegar um dos parametros do contexto que estão no ArticleProvider
    const { article } = useContext(ArticleContext);

    // executa apenas uma vez ao carregar a página
    useEffect(() =>{
        setArticleId(article.articleId);
        setText(article.text);
        setTitle(article.title);
    }, []);
    
    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const session = await getSession();
            
            const response = await fetch(`http://127.0.0.1:8000/article/update/${articleId}/`, {
                method: 'PUT',
                headers: { 
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    title,
                    text,
                    article_id: articleId,
                    user_role: session.role
                }), 
            });
            
            if (!response.ok) {
                setErrorMessage("Não foi possivel editar o artigo!");
                return;
            }       

            router.push(`/wiki/${articleId}/${title.split(' ').join('-')}`);
        } catch (error) {
            setErrorMessage("Não foi possivel editar o artigo!");
            console.log(error);
        }
    };

    return (
        <div className="create-article-container">
            <form onSubmit={(e) => {
                const confirmed = confirm('Você confirma as atualizações?');
                e.preventDefault();

                if (confirmed) {
                    handleSubmit(e);
                }
            }}>
                <div className="title-container">
                    <label htmlFor="title">Título do artigo</label>
                        <textarea 
                            type="text"
                            id="title"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            required
                    />
                </div>

                <div className="text-container">
                    <div>
                    <h2>Conteúdo do artigo</h2>
                        <textarea 
                            type="text"
                            id="text"
                            value={text}
                            onChange={(e) => 
                                {
                                    setText(e.target.value)
                                }}
                            required
                        />
                    </div>
                <div className="editor">

                    <h2>Prévia do artigo</h2>
                    <div className="preview-container">
                        <div ref={useMarkdownToHtml(text)} className="preview-text"></div>
                    </div>
                </div>
                </div>
                <div className="submitButton-container" style={{ marginTop: '20px' }}>
                    <button type="submit">Atualizar artigo</button>
                </div>

                <ErrorMessage message={errorMessage} /> 
            </form>
        </div>
    )
}