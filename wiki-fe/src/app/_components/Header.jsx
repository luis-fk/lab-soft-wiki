import React from 'react'
import '@/styles/header.css'
import Image from 'next/image'
import logo from '@/assets/images/logo.png'
import Link from 'next/link'

export default function Header() {
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
                <Link href="/cadastrar">Cadastrar</Link>
                <Link href="/login">Entrar</Link>
            </div>               
        </div>
    </>
  )
}
