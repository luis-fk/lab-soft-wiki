import React from 'react'
import '@/styles/header.css'
import Image from 'next/image'
import logo from '@/assets/images/logo.png'

export default function Header() {
  return (
    <>
        <div className="header-container">
            <a href="{% url 'encyclopedia:index' %}">
                <Image src={logo} alt="Wiki Logo" className="wiki-logo"/>
            </a>

            <a href="{% url 'encyclopedia:index' %}" className="wiki-title-link">
                <h1 className="wiki-title">WikiDengue</h1>
            </a>

            <input className="search" type="text" name="q" placeholder="Pesquisar"/>

            <div className="header-links">
                <a href="{% url 'encyclopedia:index' %}">Fórum</a>
                <a href="{% url 'encyclopedia:newPage' %}">Clima</a>
                <a href="{% url 'encyclopedia:random' %}">Cadastrar</a>
                <a href="{% url 'encyclopedia:random' %}">Entrar</a>
            </div>               
        </div>
    </>
  )
}
