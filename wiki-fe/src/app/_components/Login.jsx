"use client"
import React, { useState } from 'react';
import "@/styles/login.css";
import { useRouter } from 'next/navigation';
import ErrorMessage from './ErrorMessage';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const router = useRouter();

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (email === 'test@example.com' && password === 'password') {
            router.push('/');
        } else {
            setErrorMessage('Invalid email or password. Please try again.');
        }
    };
    
    return (
    <>
        <div className="signup-container">
            <h2>Entrar</h2>
            <form onSubmit={handleSubmit}>
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
                    <label htmlFor="password">Senha</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>

                <div className="submitButton-container">
                    <button type="submit">Entrar</button>
                </div>
            </form>

            <ErrorMessage message={errorMessage} />
        </div>
    </>
    )
}
