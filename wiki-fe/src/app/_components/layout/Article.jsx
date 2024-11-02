'use client';
import Link from 'next/link';
import React, { useState, useRef, useEffect } from 'react';
import ErrorMessage from '@/components/auth/ErrorMessage';
import Comments from '@/components/layout/Comments';
import '@/styles/wiki/article.css'; // Certifique-se de que o caminho esteja correto
import { getSession } from '@/lib/session';
import { useRouter } from 'next/navigation';
import Showdown from "showdown";

export default function Article({ params }) {
    const [session, setSession] = useState(null);
    const [errorMessage, setErrorMessage] = useState(null);
    const textView = useRef(null);
    const router = useRouter();

    const sd = new Showdown.Converter({
        tables: true,
        tasklists: true,
        strikethrough: true,
        emoji: true,
        simpleLineBreaks: true,
        openLinksInNewWindow: true,
        backslashEscapesHTMLTags: true,
        smoothLivePreview: true,
        simplifiedAutoLink: true,
        requireSpaceBeforeHeadingText: true,
        ghMentions: true,
        ghMentionsLink: '/user/{u}',
        ghCodeBlocks: true,
        underline: true,
        completeHTMLDocument: true,
        metadata: true,
        parseImgDimensions: true,
        encodeEmails: true
    });

    useEffect(() => {
        async function fetchSession() {
            const sessionData = await getSession();
            setSession(sessionData);
        }

        fetchSession();
    }, []);

    useEffect(() => {
        if (textView.current) {
            textView.current.innerHTML = sd.makeHtml(params?.content);
        }
    }, [params]);

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
        <>
            <div className='article-container'>
                {errorMessage && <ErrorMessage message={errorMessage} />}
                <div className="header-article">
                    <h1>{params?.title}</h1>
                    <div className="delete-article-container">
                        {session?.role !== 'user' && session && (
                            <Link 
                                href="#" 
                                onClick={(e) => { 
                                    const confirmed = confirm('Você tem certeza que deseja deletar o artigo?');
                                    e.preventDefault();

                                    if (confirmed) {
                                        handleDelete(e);
                                    }
                                }}
                                className="delete-link">
                                Deletar Artigo
                            </Link>
                        )}
                    </div>
                </div>
                <p className="article-content" ref={textView}></p>

                {params.isValidArticle && (
                    <Comments params={{ articleId: params?.articleId, userId: session?.userId }} />
                )}
            </div>
        </>
    );
}
