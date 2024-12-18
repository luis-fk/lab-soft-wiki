"use client"
import React, { useState, useRef } from 'react';
import { getSession } from '@/lib/session';
import { useRouter } from 'next/navigation';
import "@/styles/wiki/new-article.css";
import ErrorMessage from "@/components/auth/ErrorMessage";
import useMarkdownToHtml from '@/hooks/markdownToHtml';

export default function NewArticle() {
    const [text, setText] = useState('');
    const [title, setTitle] = useState('');
    const [errorMessage, setErrorMessage] = useState(null);

    const router = useRouter();
    
    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const session = await getSession();

            const response = await fetch('http://127.0.0.1:8000/article/create/', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    title,
                    text,
                    user_id: session.userId,
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
                <div className="submitButton-container">
                    <button type="submit">Criar artigo</button>
                </div>

                <ErrorMessage message={errorMessage} /> 
            </form>
        </div>
    )
}