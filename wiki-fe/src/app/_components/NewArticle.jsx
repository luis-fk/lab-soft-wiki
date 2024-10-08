"use client"
import React, { useState } from 'react';
// import "@/styles/new-article.css";
import "@/styles/new-article.css";

export default function NewArticle() {
    const [text, setText] = useState('');
    const [title, setTitle] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            await fetch('http://127.0.0.1:8000/article/create/', { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title,
                    text
                }), 
            });
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <div className="create-article-container">
            <h2> Novo artigo </h2>
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
