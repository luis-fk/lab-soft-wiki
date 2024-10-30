'use client'
import React, { useState, useEffect } from 'react';
import { TextField, Autocomplete } from '@mui/material';
import { getSession } from '@/lib/session';
import Link from 'next/link';
import Image from 'next/image';
import logo from '@/assets/images/logo.png';
import '@/styles/layout/header.css';
import { useRouter } from 'next/navigation';

export default function Header() {
    const router = useRouter();
    const [session, setSession] = useState(null);
    const [searchQuery, setSearchQuery] = useState('');
    const [allArticles, setAllArticles] = useState([]);
    const [hasFetched, setHasFetched] = useState(false);
    const [articlesTitle, setArticlesTitle] = useState([]);

    useEffect(() => {
        const fetchSession = async () => {
            const sessionData = await getSession();
            setSession(sessionData);
        };

        fetchSession();
    }, []);

    useEffect(() => {
        console.log("Updated allArticles:", allArticles);
    }, [allArticles]);
    

    const fetchAllArticles = async () => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/article/list/`);

            if (response.ok) {
                const data = await response.json();
    
                setAllArticles(data);

                const titles = data.map((article) => article.title);
                setArticlesTitle(titles);
                setHasFetched(true);
            } else {
                console.error("Error fetching articles:", response.statusText);
            }
        } catch (error) {
            console.error("Fetch error:", error);
        }
    };

    return (
        <div className="header-container">
             <Link href="/">
                <Image src={logo} alt="Wiki Logo" className="wiki-logo"/>
            </Link>

            <Link href="/" className="wiki-title-link">
                <h1 className="wiki-title">WikiDengue</h1>
            </Link>

            <Autocomplete
                freeSolo
                options={articlesTitle}
                inputValue={searchQuery}
                onInputChange={(event, newInputValue) => setSearchQuery(newInputValue)}
                onChange={(event, newValue) => {
                    if (newValue) {
                        const article = allArticles.find((a) => a.title === newValue);
                        router.push(`/wiki/${article.id}/${article.title.split(' ').join('-')}`);
                    }
                }}
                onFocus={() => {
                    if (!hasFetched) fetchAllArticles();
                }}
                sx={{
                    width: 600,
                    fontSize: 14,
                    backgroundColor: 'white',
                    marginLeft: '5%',
                    borderRadius: '10px',
                    '& .MuiOutlinedInput-root': {
                        borderRadius: '10px',
                    },
                }}
                renderInput={(params) => (
                    <TextField
                        {...params}
                        label="Pesquisar"
                        variant="outlined"
                        placeholder="Pesquisar artigos"
                    />
                )}
            />

            <div className="header-links">
                <Link href="/">Por que contribuir?</Link>
                <Link href="/">Fórum</Link>
                <Link href="/">Clima</Link>

                {session ? (
                    <>
                        <Link href="/logout">Sair</Link>
                        <Link href="/perfil">Perfil</Link>
                    </>
                ) : (
                    <>
                        <Link href="/cadastrar">Cadastrar</Link>
                        <Link href="/login">Entrar</Link>
                    </>
                )}
            </div>
        </div>
    );
}
