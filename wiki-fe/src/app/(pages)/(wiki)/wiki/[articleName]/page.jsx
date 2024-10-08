import React from 'react'
import Content from '@/app/_components/layout/Content'

export let metadata = {
    title: 'Artigo',
}

export default async function page({params}) {
    if (params.articleName === "dengue") {
        let data = await fetch('http://127.0.0.1:8000/random')
        let posts = await data.json()

        metadata.title = posts[0].title;
        return (
            <Content params={{title: posts[0].title, content: posts[0].text}}/>
        )
    }

    return (
        <Content params={{title: "Artigo vazio", content: "Nada a comentar"}}/>

    )
}