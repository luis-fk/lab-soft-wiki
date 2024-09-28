import React from 'react'
import dengue from '@/assets/json/dengue.json'
import Content from '@/components/Content'

export default async function page({params}) {
    if (params.articleName === "dengue") {
        let data = await fetch('http://127.0.0.1:8000/random')
        let posts = await data.json()

        return (
            <Content params={{title: posts[0].title, content: posts[0].text}}/>
        )
    }

    return (
        <Content params={{title: "Artigo vazio", content: "Nada a mostrar"}}/>
    )
}
