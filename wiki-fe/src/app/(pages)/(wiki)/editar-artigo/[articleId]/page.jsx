import React from 'react'
import EditArticle from '@/components/wiki/EditArticle';

export let metadata = {
    title: 'Criar Artigo',
}

export default function page({params}) {
    return (
        <EditArticle articleId={params.articleId}/>
    )
}