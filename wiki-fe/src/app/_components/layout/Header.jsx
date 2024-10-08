import logo from '@/assets/images/logo.png'
import Link from 'next/link'
import React from 'react'
import Image from 'next/image'
import { getSession } from '@/app/_lib/session'
import '@/styles/header.css'

export default async function Header() {
    const session = await getSession();

    return (
    <>
        <div className="header-container">
            <Link href="/">
                <Image src={logo} alt="Wiki Logo" className="wiki-logo"/>
            </Link>

            <Link href="/" className="wiki-title-link">
                <h1 className="wiki-title">WikiDengue</h1>
            </Link>

            <input className="search" type="text" name="q" placeholder="Pesquisar"/>

            <div className="header-links">
                <Link href="/">Por que contribuir?</Link>
                <Link href="/">Fórum</Link>
                <Link href="/">Clima</Link>
                
                {session
                ? <Link href="/logout">Sair</Link>
                :   <>
                        <Link href="/cadastrar">Cadastrar</Link> 
                        <Link href="/login">Entrar</Link><p></p>
                    </> 
                }
            </div>               
        </div>
    </>
    )
}
