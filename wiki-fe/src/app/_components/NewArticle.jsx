"use client"
import React, { useState } from 'react';
import { getSession } from '@/lib/session';
import "@/styles/new-article.css";

export default function NewArticle() {
    const roleAdmin = 'admin';

    const [text, setText] = useState('');
    const [title, setTitle] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const session = await getSession();

            if (!session) {
                throw new Error("Sessão não encontrada.");
            }

            if (session.role !== roleAdmin) {
                throw new Error("Você NÃO tem permissão de criar artigos.");
                console.log("estou aq e tiaizi");
            }

            await fetch('http://127.0.0.1:8000/article/create/', {
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
        } catch (error) {
            console.log(error);
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
            </form>
        </div>
    )
}
