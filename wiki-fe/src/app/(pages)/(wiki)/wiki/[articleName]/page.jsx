import React from 'react'
import Article from '@/components/layout/Article'

export let metadata = {
    title: 'Artigo',
}

export default async function page({params}) {
    if (params.articleName === "dengue") {
        const data = await fetch('http://127.0.0.1:8000/random')
        const posts = await data.json()

        metadata.title = posts[0].title;
        return (
            <Article params={{title: posts[0].title, content: posts[0].text, articleId: posts[0].id}}/>
        )
    }

    return (
        <Article params={{title: "Artigo vazio", content: "Nada a comentar"}}/>
    )
}