import React from 'react'
import dengue from '@/assets/json/dengue.json'
import Content from '@/components/Content'

export default async function page({params}) {
    let data = await fetch('http://127.0.0.1:8000/random/')
    let posts = await data.json()

    if (params.articleName === "dengue") {
        return (
            <Content params={{title: posts[0].title, content: posts[0].text}}/>
        )
    }

    return (
    <Content params={{title: "Artigo vazio", content: "Nada a mostrar"}}/>
    )
}
