'use client';
import React, { useState, useEffect } from 'react';
import ErrorMessage from '@/components/auth/ErrorMessage';
import Comments from '@/components/layout/Comments';
import '@/styles/wiki/article.css'; 
import { getSession } from '@/lib/session';
import { useRouter } from 'next/navigation';

// Importes do Context: o contexto ArticleContext e o ArticleProvider
import { useContext } from 'react';
import { ArticleContext } from '@/contexts/articleProvider';

import useMarkdownToHtml from '@/hooks/markdownToHtml';

export default function Article({ params }) {
    const [session, setSession] = useState(null);
    const [errorMessage, setErrorMessage] = useState(null);
    const router = useRouter();

    // Utiliza o contexto para pegar a função handleArticle
    const { handleArticle } = useContext(ArticleContext);

    useEffect(() => {
        async function fetchSession() {
            const sessionData = await getSession();
            setSession(sessionData);
        }

        fetchSession();
    }, []);

    const handleDelete = async (event) => {
        event?.preventDefault(); 

        try {
            const response = await fetch(`http://127.0.0.1:8000/article/delete/${params?.articleId}/`, { 
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    article_id: params?.articleId,
                    user_id: session?.userId,
                    user_role: session?.role
                }), 
            });

            if (!response.ok) {
                setErrorMessage("Ocorreu um erro ao deletar o artigo.");
                return;
            }
            router.push('/');     
        } catch (error) {
            setErrorMessage("Não foi possível deletar o artigo.");
        }
    };

    return (
            <div className='article-container'>
                {errorMessage && <ErrorMessage message={errorMessage} />}
                <div className="header-article">
                    <h1>{params?.title}</h1>
                    <div className="modify-article-container">
                        {
                        session?.role !== 'user' && session && (
                            <div className='box-modify'>
                                <button 
                                    onClick={(e) => {
                                        // Utiliza a função
                                        handleArticle(params?.title, params?.content, params?.articleId);
                                        router.push(`/editar-artigo/${params?.articleId}`);
                                    }}                                    
                                    className="edit-article">
                                    <h1>Editar</h1>
                                </button>
                                <button
                                    onClick={(e) => {
                                        const confirmed = confirm('Você tem certeza que deseja deletar o artigo?');
                                        e.preventDefault();

                                        if (confirmed) {
                                            handleDelete(e);
                                        }
                                    } }
                                    className="delete-link">
                                        <h1>Deletar</h1>
                                    </button>
                            </div>
                        )
                        }
                    </div>
                </div>
                <p className="article-content" ref={useMarkdownToHtml(params?.content)}></p>

                {params.isValidArticle && (
                    <Comments params={{ articleId: params?.articleId, userId: session?.userId, userRole: session?.role }} />
                )}
            </div>
    );
}
