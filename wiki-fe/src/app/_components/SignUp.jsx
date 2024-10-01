"use client"
import React, { useState } from 'react';
import "@/styles/sign-up.css";
import "@/styles/terms-box.css";
import Link from 'next/link';
import TermsBox from './TermsBox';

export default function SignUp() {
    const [nome, setNome] = useState('');
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [city, setCity] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [termsAccepted, setTermsAccepted] = useState(false);
    const [showTerms, setShowTerms] = useState(false); 

    const toggleTerms = () => {
        setShowTerms(!showTerms);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            await fetch('http://127.0.0.1:8000/user/create/', { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username,
                    password,
                    email,
                }), 
            });
        } catch (error) {
            console.log(error);
        }
    };

    return (
    <>
        {
            <div className="signup-container">
                <h2>Cadastre-se</h2>
                <form onSubmit={handleSubmit}>
                    <div>
                        <label htmlFor="username">Usuário</label>
                        <input
                            type="text"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>
                    
                    <div>
                        <label htmlFor="password">Senha</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>

                    <div>
                        <label htmlFor="confirmPassword">Confirme a senha</label>
                        <input
                            type="password"
                            id="confirmPassword"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required
                        />
                    </div>

                    <div>
                        <label htmlFor="nome">Nome</label>
                        <input
                            type="text"
                            id="nome"
                            value={nome}
                            onChange={(e) => setNome(e.target.value)}
                            required
                        />
                    </div>

                    <div>
                        <label htmlFor="email">Email</label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>

                    <div>
                        <label htmlFor="city">Cidade</label>
                        <input
                            type="text"
                            id="city"
                            value={city}
                            onChange={(e) => setCity(e.target.value)}
                        />
                    </div>

                    <div className="terms-container">
                        <input
                            type="checkbox"
                            id="terms"
                            checked={termsAccepted}
                            onChange={(e) => setTermsAccepted(e.target.checked)}
                            required
                        />

                        <Link 
                        href="#" 
                        onClick={(e) => { 
                            toggleTerms();
                            e.preventDefault(); 
                        }}
                        className="terms-link">  
                            Eu aceito os termos de uso
                        </Link>
                    </div>

                    <div className="submitButton-container">
                        <button type="submit">Cadastrar</button>
                    </div>
                </form>
            
                {showTerms && (
                    <div className="terms-modal">
                    <TermsBox />
                    <button onClick={toggleTerms}>Voltar ao Cadastro</button>
                    </div>
                )}

            </div>
         }
    </>
    );
}
