'use client'
import { useRouter } from 'next/navigation';
import React, { useState } from 'react';
import ErrorMessage from './ErrorMessage';
import { authenticate } from '@/lib/session'
import "@/styles/auth/login.css";
import Link from 'next/link';

export default function Login() {
    const [errorMessage, setErrorMessage] = useState(null);
    const router = useRouter();

    async function handleSubmit(event) {
        event.preventDefault()
     
        const formData = new FormData(event.target)
        const result = await authenticate(formData);
    
        if (result.errorMessage) {
            setErrorMessage(result.errorMessage);
        } else {
            router.push('/');
        }
      }

    return (
    <>
        <div className="login-container">
            <h2>Entrar</h2>
            <form onSubmit={handleSubmit}>

            <div>
                <label htmlFor="email">Email</label>
                <input type="email" name="email" placeholder="Email" required />
            </div>

            <div>
                <label htmlFor="password">Senha</label>
                <input type="password" name="password" placeholder="Password" required />
            </div>

            <p>Ainda nao possui uma conta? <Link href="/cadastrar">Cadastre-se</Link></p>

            <div className="submitButton-container">
                <button type="submit">Entrar</button>
            </div>
            </form>
            
            <ErrorMessage message={errorMessage} />
        </div>
    </>
    )
}
