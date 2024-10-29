'use client';
import Link from 'next/link';
import React, { useState, useRef, useEffect } from 'react';
import '@/styles/wiki/article.css';
import Comments from '@/components/layout/Comments';
import { getSession } from '@/lib/session';
import { useRouter } from 'next/navigation';
import Showdown from "showdown";

export default function Article({ params }) {
    const [session, setSession] = useState(null);
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

            if (response.ok) {
                router.push('/'); 
            } else {
                console.error('Erro ao deletar o artigo:', response.statusText);
            }
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <>
            <div className='article-container'>
                <div className="header-article" style={{ display: 'flex', alignItems: 'center', marginTop: '-20px' }}>
                    <h1>{params?.title}</h1>
                    <div style={{ marginLeft: 'auto' }}>
                        {session?.role !== 'user' && session && (
                            <Link style={{  
                                width: '100px',
                                padding: '10px',
                                backgroundColor: 'red',
                                borderRadius: '8px',
                                boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
                                textDecoration: 'none',
                                color:'white'
                            }}
                            href="#" 
                            onClick={(e) => { 
                                const confirmed = confirm('Você tem certeza que deseja deletar o artigo?');
                                e.preventDefault();

                                if(confirmed) {
                                    handleDelete(e);
                                }
                            }}
                            className="delete-link">
                                Deletar Artigo
                            </Link>
                        )}
                    </div>
                </div>
                <p style={{ marginTop: '20px' }} ref={textView}></p>

                {params.isValidArticle && (
                    <Comments params={{ articleId: params?.articleId, userId: session?.userId }} />
                )}
            </div>
        </>
    );
}
