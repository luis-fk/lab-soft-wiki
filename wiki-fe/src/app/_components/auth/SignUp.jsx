"use client"
import "@/styles/auth/sign-up.css";
import Link from 'next/link';
import TermsBox from '@/components/auth/TermsBox';
import ErrorMessage from './ErrorMessage';
import { authenticate } from '@/lib/session'
import { useRouter } from 'next/navigation';
import React, { useState } from 'react';

export default function SignUp() {
    const [termsAccepted, setTermsAccepted] = useState(false);
    const [showTerms, setShowTerms] = useState(false); 
    const [errorMessage, setErrorMessage] = useState(null);
    
    const router = useRouter();

    const toggleTerms = () => {
        setShowTerms(!showTerms);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        const formData = new FormData(event.target)

        if (formData.get('password') !== formData.get('confirmPassword')) {
            setErrorMessage('As senhas devem ser iguais');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/user/create/', { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: formData.get('name'),
                    email: formData.get('email'),
                    password: formData.get('password'),
                    city: formData.get('city'),
                }), 
            });

            if (!response.ok) {
                const data = await response.json();
                setErrorMessage(data.error);
                return;
              }

            await authenticate(formData);
            router.push('/');

        } catch (error) {
            setErrorMessage(error.error);
        }
    };

    return (
    <>
        {
            <div className="signup-container">
                <h2>Cadastre-se</h2>
                <form onSubmit={handleSubmit}>
                    <div>
                        <label htmlFor="nome">Nome</label>
                        <input type="text" name="name" placeholder="Nome" required />
                    </div>

                    <div>
                        <label htmlFor="email">Email</label>
                        <input type="email" name="email" placeholder="Email" required />
                    </div>

                    <div>
                        <label htmlFor="password">Senha</label>
                        <input type="password" name="password" placeholder="Senha" required />
                    </div>

                    <div>
                        <label htmlFor="confirmPassword">Confirme a senha</label>
                        <input type="password" name="confirmPassword" placeholder="Confime a senha" required />
                    </div>

                    <div>
                        <label htmlFor="city">Cidade</label>
                        <input type="text" name="city" placeholder="Cidade"
                        />
                    </div>

                    <div className="terms-container">
                        <input type="checkbox" name="terms" checked={termsAccepted}
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

                    <ErrorMessage message={errorMessage} />
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
