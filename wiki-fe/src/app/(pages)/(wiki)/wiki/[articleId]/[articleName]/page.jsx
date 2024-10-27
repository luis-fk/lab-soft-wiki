import React from 'react';
import Article from '@/components/layout/Article';

export let metadata = {
    title: 'Artigo',
}

export default async function Page({ params }) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/article/list/${params.articleId}`);
        
        if (!response.ok) {
            throw new Error('Artigo não encontrado');
        }

        const article = await response.json();
        metadata.title = article.title;
        return (
            <Article
                params={{
                    title: article.title,
                    content: article.text,
                    articleId: article.id,
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
