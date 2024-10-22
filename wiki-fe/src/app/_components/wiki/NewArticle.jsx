"use client"
import React, { useState } from 'react';
import { getSession } from '@/lib/session';
import { useRouter } from 'next/navigation';
import "@/styles/wiki/new-article.css";
import ErrorMessage from "@/app/_components/error/ErrorMessage";

export default function NewArticle() {
    const roleAdmin = 'admin';

    const [text, setText] = useState('');
    const [title, setTitle] = useState('');
    const [errorMessage, setErrorMessage] = useState(null);

    const router = useRouter();

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const session = await getSession();

            if(session.role !== roleAdmin) {
                return router.push('/');
            }

            const response = await fetch('http://127.0.0.1:8000/article/create/', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    title,
                    text,
                    user_id: session.userId
                }), 
            });

            
            if (!response.ok) {
                const data = await response.json();
                setErrorMessage(data.error);
                return;
            }

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
                    <label htmlFor="text">Conteúdo do artigo</label>
                        <textarea 
                            type="text"
                            id="text"
                            value={text}
                            onChange={(e) => setText(e.target.value)}
                            required
                        />
                </div>
                <div className="submitButton-container">
                    <button type="submit">Criar artigo</button>
                </div>

                <ErrorMessage message={errorMessage} /> 
            </form>
        </div>
    )
}
