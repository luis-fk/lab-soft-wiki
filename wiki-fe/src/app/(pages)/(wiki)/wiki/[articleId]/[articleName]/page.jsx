import React from 'react';
import Article from '@/components/layout/Article';

export let metadata = {
    title: 'Artigo',
}

export default async function Page({ params }) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/article/detail/${params.articleId}`, {
            method: 'GET',
            cache: 'no-store',
        });
        
        const article = await response.json();

        metadata.title = article.title;

        try {
            await fetch(`http://127.0.0.1:8000/article/update/${article.id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ views: article.views + 1 }),
          });   
          } catch {}

        return (
            <Article
                params={{
                    title: article.title,
                    content: article.text,
                    articleId: article.id,
                    articleViews: article.views,
                    isValidArticle: true,
                }}
            />
        );
    } catch (error) {
        return (
            <Article
                params={{
                    title: 'Artigo não existe',
                    content: 'Contribua para o WikiDengue!',
                    isValidArticle: false,
                }}
            />
        );
    }
}
