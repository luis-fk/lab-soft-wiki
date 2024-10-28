'use client'
import React, { useEffect, useState } from 'react';
import '@/styles/layout/body.css'
import Link from 'next/link'

export default function Body({ children }) {
    const [articles, setArticles] = useState([]);

    useEffect(() => {
        const fetchArticles = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:8000/article/list/`, {
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json' },
                });
                
                const data = await response.json();

                if (!response.ok) {
                    setErrorMessage(data.error);
                    return;
                }

                setArticles(data);
            } catch (err) {
                setErrorMessage('Um erro ocorreu ao tentar carregar os artigos.');
            }
        };

        fetchArticles();
    }, []);
  
  return (
      <div className="body-container">
          <div className="sidebar">
                <h2>Navegação</h2>

                <Link href="/">Início</Link>
                {articles.map((article) => (
                    <Link key={article.id} href={`/wiki/${article.id}/${article.title.split(' ').join('-')}`}>
                        {article.title}
                    </Link>
                ))}
          </div>

          {children}
      </div>
  )
}