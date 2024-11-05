"use client"
import React, { useState, useRef, useEffect } from 'react';
import { getSession } from '@/lib/session';
import { useRouter } from 'next/navigation';
import "@/styles/wiki/new-article.css";
import ErrorMessage from "@/app/_components/auth/ErrorMessage";
import Showdown from "showdown";

// Importes do Context 
import { ArticleContext } from '@/app/contexts/articleProvider';
import { useContext } from 'react';

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
        //renderiza
        setPreview(article.text);

    }, []);


    const sd = new Showdown.Converter(
        {
            tables: true,
            tasklists: true,
            strikethrough: true,
            emoji: true,
            simpleLineBreaks: true,
            openLinksInNewWindow: true,
            backslashEscapesHTMLTags: true,
            smoothLivePreview: true,
            simplifiedAutoLink: true,
            simpleLineBreaks: true,
            requireSpaceBeforeHeadingText: true,
            ghMentions: true,
            ghMentionsLink: '/user/{u}',
            ghCodeBlocks: true,
            emoji: true,
            underline: true,
            completeHTMLDocument: true,
            metadata: true,
            parseImgDimensions: true,
            encodeEmails: true,
            openLinksInNewWindow: true
        });

    const previewRef = useRef(null);
    
    const setPreview = (text) => {
        if (previewRef.current) {
            previewRef.current.innerHTML = sd.makeHtml(text);
        }
    }
    
    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const session = await getSession();

            const response = await fetch('http://127.0.0.1:8000/article/update/', {
                method: 'POST',
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

            const data = await response.json();
            
            if (!response.ok) {
                setErrorMessage(data.error);
                return;
            }       

            router.push(`/wiki/${data.artigo_id}/${title.split(' ').join('-')}`);
        } catch (error) {
            const data = await response.json();
            setErrorMessage(data.error);
            return;
        }
    };

    return (
        <div className="create-article-container">
            <form onSubmit={handleSubmit}>
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
                                    setPreview(e.target.value)
                                }}
                            required
                        />
                    </div>
                <div className="editor">

                    <h2>Prévia do artigo</h2>
                    <div className="preview-container">
                        <div ref={previewRef} className="preview-text"></div>
                    </div>
                </div>
                </div>
                <div className="submitButton-container">
                    <button type="submit">Atualizar artigo</button>
                </div>

                <ErrorMessage message={errorMessage} /> 
            </form>
        </div>
    )
}